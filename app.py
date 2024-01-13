import os

import requests
from flask import Flask, redirect, render_template, request, session
from flask_socketio import SocketIO, emit
from functools import wraps

from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Note about Flow instances: I am not sure if it is correct to create a flow instance in every method, 
# or if it is better to have a global flow instance. 

# OAuth 2.0 secrets file. When creating a flow instance, this gives the PATH to the file. 
# If you client secret is in a different folder, change to that PATH instead.
client_secret = "client_secret.json"

# OUauth 2.0 access to user account and livestream details. 
scopes = ["https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtube",
          "https://www.googleapis.com/auth/youtube.force-ssl"]

# API service and version
api_service_name = "youtube"
api_version = "v3"

# Create app and give it your secret key. Create socketio for dynamic updates
app = Flask(__name__)
app.config["SECRET_KEY"] = "Insert your client secret here" # Insert your client secret here
socketio = SocketIO(app)

# Ensure that user is logged into their Youtube account. 
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "credentials" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper


@app.route("/")
@login_required
def index():
    return render_template("index.html")
    
@app.route("/activechat")
@login_required
def activechat():
    # Ensure credentials are in the session.
    # NOTE: this way of giving credentials is vulnerable to attacks from a local user giving their own session. 
    if "credentials" not in session:
        return redirect("/login")
    credentials = Credentials(
        **session["credentials"]
    )
    # Create youtube client to make requests
    youtube = build(
        api_service_name,
        api_version,
        credentials=credentials
    )
    # API request and response
    api_request = youtube.liveBroadcasts().list(
        part="snippet",
        broadcastStatus="active"
    )
    api_response = api_request.execute()
    # NOTE: this assumes that you only have 1 active livestream.
    # Otherwise, you may not get the correct livestream chat when getting the 0 indexed stream 
    try: 
        livechatid = api_response["items"][0]["snippet"]["liveChatId"]
        session["livechatid"] = livechatid
    except IndexError: # you either have multiple or 0 livestreams active. 
        livechatid = None
        session["livechatid"] = None # redundancy for sessions. Still susceptible to local session changes.
    
    return render_template("activechat.html", livechatid=livechatid)

@app.route("/scroller")
@login_required
def scroller():
    return render_template("scroller.html")


@app.route("/login")
def login():
    # Create flow instance to manage OAuth 2.0; ensure that redirect uri matches the one you authorized
    flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secret,
        scopes=scopes,
        redirect_uri="http://localhost:5000/callback"
    )

    # Generate url to authorize app to access user's account
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type="offline",
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes="true")
    
    # Add login to current session
    session["state"] = state
    session.modified = True
    
    # Send to authorization page
    return redirect(authorization_url)
    

@app.route("/callback")
def callback():
    # Specify the state when creating the flow in the callback so that it can be
    # verified in the authorization server response.
    flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secret,
        scopes=scopes,
        state=session["state"], # automatically checks if sessions are the same
        redirect_uri="http://localhost:5000/callback"
    )
    
    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
   
    # Store credentials in session
    credentials = flow.credentials
    session["credentials"] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    return redirect("/")


@app.route("/revoke")
@login_required
def revoke():
    if "credentials" not in session:
        return ("You need to <a href='/login'>login</a> before revoking credentials.")
    
    credentials = Credentials(
        **session["credentials"]
    )

    revoke = requests.post('https://oauth2.googleapis.com/revoke',
        params={'token': credentials.token},
        headers = {'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        # Clear session so user is no longer signed in. 
        # If making a production app, need more elaborate way to ensure user can't stay on the site without having credentials. 
        session.clear()
        return('Credentials successfully revoked. <a href="/">Home</a>')
    else:
        return('An error occurred. Return to homepage <a href="/">Home</a>')


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# SocketIO decorators will be here
@socketio.on("connect")
def connect():
    print('connected')
    

@socketio.on("scroll")
def handle_scroll():
    print("Starting scroll")
    while True:
        messages = getMessages()
        for message in messages:
            id = message["id"]
            user = message["authorDetails"]["displayName"]
            text = message["snippet"]["displayMessage"] # NOTE: Youtube API automatically escapes special characters. Can directly put the response into html 
            package = {"id": id, "user": user, "message": text}
            emit("message", package, broadcast = False) # broadcast = false means other users will not get this new data.
        socketio.sleep(1) # Adjust this to change API call rate. 


# Helper functions
def messageRequest(youtube, pageToken):
    request = youtube.liveChatMessages().list(
        liveChatId=session["livechatid"],
        part="snippet,authorDetails",
        pageToken=pageToken
    )
    response = request.execute()
    return response

def getMessages():
        if ("credentials" and "livechatid") not in session:
            return redirect("/login")
        credentials = Credentials(
            **session["credentials"]
        )
        youtube = build(
            api_service_name,
            api_version,
            credentials=credentials
        )
        
        # Refresh pageToken to get most recent messages. A more elegant solution would be preferred.  
        # checking message within current session; likely came from a previous message check
        try: 
            response = messageRequest(youtube, session["pageToken"])
        # checking messages for the first time. Want to load new messages from this point on. 
        except: 
            firstResponse = messageRequest(youtube, None)
            newToken = firstResponse["nextPageToken"]
            response = messageRequest(youtube, newToken)

        session["pageToken"] = response["nextPageToken"]
        return response["items"]


if __name__ == "__main__":
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    
    # Specify a hostname and port that are set as a valid redirect URI
    # for your API project in the Google API Console.
    socketio.run(app, host="localhost", port=5000, debug=True) 