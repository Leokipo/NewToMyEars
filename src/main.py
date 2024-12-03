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

# def getSongsofGenre(token, genre, offset):
#     url = "https://api.spotify.com/v1/search"
#     query = f"?q=genre:{genre}&type=track&limit=50&offset={offset}"
#     query_url = url + query
#     headers = getAuthHeader(token)
#
#     result = get(query_url, headers=headers)
#     json_result = json.loads(result.content)["tracks"]["items"]
#     return json_result

def getPlaylistSongs(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = getAuthHeader(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)["playlist"]["tracks"]["items"]
    return json_result

def getPlaylistsofGenre(token, genre, offset):
    url = "https://api.spotify.com/v1/search"
    query = f"?q={genre}&type=playlist&limit=50&offset={offset}"
    query_url = url + query
    headers = getAuthHeader(token)

    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["playlists"]["items"]
    return json_result

def getSongsofPlaylist(playlists):
    songs = []
    token = getToken()
    for item in playlists:
        if item is None:
            continue
        playlist_id = item["id"]
        print(playlist_id)
        tracks = getPlaylistSongs(token, playlist_id)


token = getToken()
genre = "rap"
result = []
total_songs = 0
for i in range(0,20):
    result += getPlaylistsofGenre(token, genre, i*50)
getSongsofPlaylist(result)

"""
Loop for getting random popularity scores to access songs stored in the multimap and redblack data structures
Each score is a multiple of 5 starting from 10, summed with a random integer 0-4
"""
multimapSongs = []
redblackSongs = []
for i in range(0,10):
    randomScore = 10 + (i * 5) + random.randint(0, 4)
    # using randomScore, get a song from multimap and redblack and append to corresponding list