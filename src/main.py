# Followed tutorial from YouTube on SpotifyAPI calls (https://www.youtube.com/watch?v=WAmEZBEeNmg&ab_channel=AkamaiDeveloper)
import random
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

def populateSongs(storage, genre, frame):
    # clear current frame of song ids
    for label in frame.winfo_children():
        label.destroy()

    token = getToken()
    # store songs from playlists of the genre
    result = []
    for i in range(0, 15):
        result += getPlaylistsofGenre(token, genre, i * 35)

    songs = getSongsofPlaylists(result)

    # store songs in inputted data structure
    for song_id, popularity in songs:
        storage.insert(popularity, song_id)

    generated_songs = storage.create_playlist()

    # display songs in a new frame
    for song in generated_songs:
        tk.Label(frame, text=song, font=("Arial", 8)).pack()
    frame.pack(padx=5, pady=5)

"""
GUI Implementation
"""
import tkinter as tk
def displayGenreSelection():
    root = tk.Tk()
    root.geometry("700x700")
    root.title("NewToMyEars")

    tk.Label(root, text="Welcome to NewToMyEars!", font=("Arial", 20)).pack(padx=10, pady=10)
    tk.Label(root, text="Type a genre to make a playlist of new music", font=("Arial", 16)).pack(padx=10, pady=10)

    # retrieve genre input from Entry field
    genreVar = tk.StringVar()
    tk.Entry(root, textvariable=genreVar, font=("Arial", 16)).pack(padx=10, pady=10)

    def makeRedBlack():
        genre = genreVar.get().lower()
        storage = RedBlackTree()
        populateSongs(storage, genre, frame)
    def makeMultimap():
        genre = genreVar.get().lower()
        storage = multimap()
        populateSongs(storage, genre, frame)

    # buttons for activating storage container
    tk.Button(root, text="Generate Playlist Using Red Black Tree", command=makeRedBlack).pack(padx=10, pady=10)
    tk.Button(root, text="Generate Playlist Using Multimap", command=makeMultimap).pack(padx=10, pady=10)

    # frame for displaying song ids
    frame = tk.Frame(root)

    root.mainloop()

displayGenreSelection()


"""token = getToken()
genre = input("Genre to explore: ")
print(f"Generating {genre} songs...")
result = []
for i in range(0,15):
    result += getPlaylistsofGenre(token, genre, i*35)

songs = getSongsofPlaylists(result)


data_structure = input("Data Structure to use (0 for red black tree, 1 for multimap): ")
while data_structure != "0" and data_structure != "1":
    data_structure = input("Error. Incorrect input.\nData Structure to use (0 for red black tree, 1 for multimap): ")
if data_structure == "0":
    storage = RedBlackTree()
else:
    storage = multimap()

for song_id, popularity in songs:
    storage.insert(popularity, song_id)

print(storage.create_playlist())"""


