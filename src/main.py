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

def searchArtist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = getAuthHeader(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("No artist with name ",artist_name, " found.")
        return None
    return json_result[0]

def getSongsByArtist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = getAuthHeader(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

token = getToken()
result = searchArtist(token, "Tame")
artist_id = result["id"]
top_songs = getSongsByArtist(token, artist_id)
for song in top_songs:
    print(song["name"])
