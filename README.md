# Youtube Live Chat Scroller
### This app attempts to recreate the bullet chat scrolling of live stream platforms like Bilibili and Niconico using YouTube's data API. The intended purpose of the app is to be used as an OBS chat overlay. 

## Creating a Google OAuth 2.0 Client 
##### Create an OAuth client using the instructions below or by using [this video](https://www.youtube.com/watch?v=D8DMj2lQMwo)
### Create a new project in the [Google Developer Console](https://console.developers.google.com/project)
### Go to the [Google API library](https://console.cloud.google.com/apis/library) 
* Search for and enable "YouTube Data API v3" 
### Under "APIs & Services", go to the ["Credentials"](https://console.cloud.google.com/apis/credentials) tab
* Click the "Create Credentials" button
* Click the "OAuth client ID" button
* For application type, choose "web application"
* For "Authorized redirect URIs", put whatever test URI you will be using. If you are unsure, simply put "http://localhost/callback"
* ***Download the client secret json***
### Go to the [OAuth consent screen](https://console.cloud.google.com/auth) 
* Go to the Branding section to fill out information pertaining to the app
* Go to the Audience section and fill out accessibility settings for the app
* ***Under Test users, add any account you want to access the app. If you want to use it yourself, add your own gmail***

### Add the following scopes to the scopes page:
- /auth/youtube.readonly
- /auth/youtube
- /auth/youtube.force-ssl

## Editing the Project folder
* Download the modules in the "requirements.txt" file.
* Replace "client_secret.json" with your own secret JSON from your OAuth client.
* On line 15, ensure that the PATH for your client secret is correct.
* ***On the final line of app.py, make sure the host address matches the redirect URI you gave your OAuth client.*** 


## Using the app
* Run the app in your terminal using "python app.py".
* Login using the test user account you gave the OAuth client. Grant the app permission to access your YouTube data.
* Click the "Check Active Stream Button". If you do not have an active stream, start your YouTube stream and try again.
* You will be given a green button to redirect you to the scrolling page once a stream is detected.
* Click the "Start Chat Scrolling" button
* Any messages typed in your live chat will now appear on the webpage. 
* Simply press the red button to end scrolling.

## Future improvements
* The server currently uses Flask session variables during the OAuth process. Using an actual database would be preferred for a production level app.
* Adding more chat customization. Could include ways to change the text size, colour, and scroll speed of the messages. Changing the scrolling direction would also be interesting. 
* Adding support for emotes, superchats, and stickers.
