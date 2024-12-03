# Followed tutorial from YouTube on SpotifyAPI calls (https://www.youtube.com/watch?v=WAmEZBEeNmg&ab_channel=AkamaiDeveloper)
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

def getSongsofGenre(token, genre, offset):
    url = "https://api.spotify.com/v1/search"
    query = f"?q=genre:{genre}&type=track&limit=50&offset={offset}"
    query_url = url + query
    headers = getAuthHeader(token)

    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    return json_result

def getPlaylistsofGenre(token, genre, offset):
    url = "https://api.spotify.com/v1/search"
    query = f"?q={genre}&type=playlist&limit=50&offset={offset}"
    query_url = url + query
    headers = getAuthHeader(token)

    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["playlists"]["items"]
    return json_result

token = getToken()
genre = "rap"
result = []
total_songs = 0
for i in range(0,20):
    result += getPlaylistsofGenre(token, genre, i*50)
for item in result:
    if item is None:
        continue
    total_songs += item["tracks"]["total"]