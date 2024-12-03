# Followed tutorial from YouTube on SpotifyAPI calls (https://www.youtube.com/watch?v=WAmEZBEeNmg&ab_channel=AkamaiDeveloper)
import random
import base64

from dotenv import load_dotenv
import json
import os
from requests import post, get

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
                print("fail")
                continue
            song_pair = (name, popularity)
            songs.append(song_pair)
    return songs


token = getToken()
genre = input("Genre to explore: ")
result = []
total_songs = 0
for i in range(0,15):
    result += getPlaylistsofGenre(token, genre, i*50)
songs = getSongsofPlaylists(result)
print(len(result))
print(len(songs))
for song in songs:
    print(song[0], song[1])