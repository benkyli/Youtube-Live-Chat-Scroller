# Youtube Live Chat Scroller
#### Video Demo:  [YouTube Live Chat Scroller](https://youtu.be/LVeqXZTBPCY)
#### Description: This webapp attempts to recreate the bullet chat scrolling of live stream platforms like Bilibili and Niconico using YouTube's data API. The intended purpose of the app is to be used as an OBS chat overlay. 

## Creating a Google OAuth 2.0 Client (September 2023)
#### If the below instructions are unclear, try [this video](https://www.youtube.com/watch?v=1XUu7-yIoUY&t=383s&pp=ygUReW91dHViZSBhcGkgb2F1dGg%3D) or [this video](https://www.youtube.com/watch?v=irhhMLKDBZ8&t=351s)
### **Create a new project in the [Google Developer Console](https://console.developers.google.com/project)**
### Go to the [Google API library](https://console.cloud.google.com/apis/library) 
##### Search for and enable "YouTube Data API v3" 
### Under "APIs & Services", go to the "Credentials" tab.
##### Click the "Create Credentials" button
##### Click the "OAuth client ID" button
##### For application type, choose "web application"
##### For "Authorized redirect URIs", put whatever test site you will be using. If you are unsure, simply put "http://localhost/callback"
***Download the client secret json***
### Go to the OAuth consent screen and click "edit app"
##### Fill in the "App information" page with your own details
##### Add the following scopes to the scopes page:
- /auth/youtube.readonly
- /auth/youtube
- /auth/youtube.force-ssl
##### Under Test users, add any account you want to access the webapp. If you want to use it yourself, add your own gmail.

## Editing the Project folder
#####  Download the modules in the "requirements.txt" file. You can use a virtual environment if you'd like.
#####  Replace the "client_secret.json" with the client secret JSON you downloaded when creating the OAuth client
#####  On line 30, put your own client secret here. Check the google API console or the client secret file if you are unsure.
##### ***On the final line of the project, make sure the host address and/or match with the redirect URI you put during the OAuth client creation.*** 


## Using the app
##### If you used a virtual environment, activate it now.
##### Run the app by typing "Python app.py". This assumes you did not change the app's name. Otherwise, make sure you run the app using it's correct name.
##### At the login screen, login using the test user account you gave the OAuth client. Grant the app permission to access your YouTube data.
##### Click the "Check Active Stream Button". If you did not have an active stream, start your YouTube stream and click the button again. 
##### If you did have an active stream, you will be given a green button to redirect you to the scrolling text screen. 
##### Click the "Start Chat Scrolling" button
##### Any chat messages typed in your live chat will now appear on the webpage. 

## How to Stop Scrolling
#### Type "CTRL+C" in the python terminal to stop the app from fetching your YouTube livechat data. 
##### Stopping the while loop used to call the YouTube API turned out to be much more complicated than expected. In order to stop the while loop, it would require you to run it on a separate thread. However, the while loop uses the session variable from Flask, which becomes inaccessible when on a different thread. Instead of using a Flask session variable, it would have been better to create a database to store the required credentials and page tokens needed to make the API calls. However, that was a large amount of extra work that I currently do not have time for. Apologies to anybody that actually tries to use this app. 

## Future improvements
#### Beyond using a database and creating a more intuitive way of stopping the chat scroller, there were many more quality of life changes that I wanted to include in the project. These included ways to change the text size, colour, and scroll speed of the messages. Being able to change the direction of the text scroll would have also been nice. 

#### Adding functionality for emotes, superchats, and stickers would also have been a good addition to the project. 
