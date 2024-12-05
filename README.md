
NewToMyEars - A Spotify tool for generating playlists of lesser-known music

To use this tool, you must create a Spotify Web API app at https://developer.spotify.com/.
Once the app is created, populate the .env file with the required variables:\
\
        CLIENT_ID: an id created by Spotify to recognize the app.\
	CLIENT_SECRET: a secret that can be changed, don't share this with others.\
	REDIRECT_URI: a redirect URI that you create for redirecting authentication requests.\

After these setup steps are completed, the code can be run.\
Running the main.py file will show a GUI for user input.\
\
Initial info required by the GUI:\
\
	**Username**: This is your Spotify username *not your display name*. This is required to create a playlist in your account.
 		To find your account username in the Spotify app, select your profile in at the top right of the screen. Then, select "Account." This should bring 		you to another webpage. Here, under the "Account" section, select "Edit profile." The long string of characters under "Username" is what you need 		to copy.\
   \
	**Genre**: This is a keyword that will be used to find related music. We recommend that you search for a genre.\
\
After this information is inputted, you can select which data structure to store generated songs in:\
	**Red-black tree** implementation or **multimap** implementation.\
	This will have no effect on the resulting playlist, both will contain random songs of varying popularity.\
\
This generation will take some time as many songs will populate the data structure.\
\
After the songs have been generated, you will have two more tasks:\
	**1.** Input the name of your new playlist.\
	**2.** Input the description of your new playlist (this is optional).\
\
Finally, click the "Generate Playlist" button to create the playlist. It will automatically populate in your Spotify account.
