# Followed tutorial from YouTube on SpotifyAPI calls (https://www.youtube.com/watch?v=WAmEZBEeNmg&ab_channel=AkamaiDeveloper)
import base64

from dotenv import load_dotenv
import json
import os
from requests import post, get

from redblack import RedBlackTree
from multimap import multimap

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')

def getToken():
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

def getAuthHeader(token):
    return {"Authorization": "Bearer " + token}

def getPlaylistsofGenre(token, genre, offset):
    url = "https://api.spotify.com/v1/search"
    query = f"?q={genre}&type=playlist&limit=1&offset={offset}"
    query_url = url + query
    headers = getAuthHeader(token)

    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["playlists"]["items"]
    return json_result

def getPlaylistSongs(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = getAuthHeader(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    return json_result

def getSongsofPlaylists(playlists):
    songs = []
    token = getToken()
    for item in playlists:
        if item is None:
            continue
        playlist_id = item["id"]
        playlist_tracks = getPlaylistSongs(token, playlist_id)
        for tracks in playlist_tracks:
            try:
                name = tracks["track"]["id"]
                popularity = tracks["track"]["popularity"]
            except:
                continue # Track is null or something
            song_pair = (name, popularity)
            songs.append(song_pair)
    return songs

"""
GUI Implementation
"""
import tkinter as tk
# USER AUTHENTICATION
import spotipy
from spotipy.oauth2 import SpotifyOAuth
def createUserPlaylist(username, playlist_name, playlist_description, song_ids):
    scope = "playlist-modify-private"

    token = SpotifyOAuth(scope=scope, username=username, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    spotifyObject = spotipy.Spotify(auth_manager=token)

    # create a new playlist
    new_playlist = spotifyObject.user_playlist_create(user=username, name=playlist_name, public=False, description=playlist_description)
    spotifyObject.playlist_add_items(new_playlist["id"], song_ids)

def generateSongs(storage, genre, username, frame):
    # clear current frame of playlist generation
    for widget in frame.winfo_children():
        widget.destroy()

    # tell user the songs are being generated
    tk.Label(frame, text="Generating songs...", font=("Arial", 12)).pack(padx=10, pady=10)
    frame.pack()

    token = getToken()
    # store songs from playlists of the genre
    result = []
    for i in range(0, 15):
        result += getPlaylistsofGenre(token, genre, i * 35)

    songs = getSongsofPlaylists(result)

    # store songs in inputted data structure
    for song_id, popularity in songs:
        storage.insert(popularity, song_id)

    # get random songs of each popularity range
    generated_songs = storage.create_playlist()

    # songs have been generated
    tk.Label(frame, text="Songs have been generated!", font=("Arial", 12)).pack(padx=10, pady=10)

    # ask for playlist name/description in a new frame
    tk.Label(frame, text="Enter playlist name", font=("Arial", 16)).pack(padx=10, pady=10)
    playlist_name_var = tk.StringVar()
    tk.Entry(frame, textvariable=playlist_name_var, font=("Arial", 16)).pack(padx=10)
    tk.Label(frame, text="Enter playlist description", font=("Arial", 16)).pack(padx=10, pady=10)
    playlist_description_var = tk.StringVar()
    tk.Entry(frame, textvariable=playlist_description_var, font=("Arial", 16)).pack(padx=10)

    # button to generate playlist
    def generatePlaylist():
        playlist_name = playlist_name_var.get()
        playlist_description = playlist_description_var.get()
        createUserPlaylist(username, playlist_name, playlist_description, generated_songs)

        tk.Label(frame, text="Playlist generated! Check your Spotify account.")


    tk.Button(frame, text="Generate Playlist", command=generatePlaylist).pack(padx=10, pady=10)

def displayGenreSelection():
    root = tk.Tk()
    root.geometry("700x700")
    root.title("NewToMyEars")

    tk.Label(root, text="Welcome to NewToMyEars!", font=("Arial", 20)).pack(padx=10, pady=10)

    # user authentication
    tk.Label(root, text="Enter your Spotify Username", font=("Arial", 16)).pack(padx=10, pady=10)
    user_var = tk.StringVar()
    tk.Entry(root, textvariable=user_var, font=("Arial", 16)).pack(padx=10)

    # genre input
    tk.Label(root, text="Type a genre to make a playlist of new music", font=("Arial", 16)).pack(padx=10, pady=10)
    genreVar = tk.StringVar()
    tk.Entry(root, textvariable=genreVar, font=("Arial", 16)).pack(padx=10)

    def makeRedBlack():
        genre = genreVar.get().lower()
        username = user_var.get()
        storage = RedBlackTree()
        generateSongs(storage, genre, username, frame)
    def makeMultimap():
        genre = genreVar.get().lower()
        username = user_var.get()
        storage = multimap()
        generateSongs(storage, genre, username, frame)

    # buttons for activating storage container
    tk.Button(root, text="Generate Songs Using Red Black Tree", command=makeRedBlack).pack(padx=10, pady=10)
    tk.Button(root, text="Generate Songs Using Multimap", command=makeMultimap).pack(padx=10, pady=10)

    # frame for displaying song ids
    frame = tk.Frame(root)
    frame.pack()

    root.mainloop()

displayGenreSelection()