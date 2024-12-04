# Followed tutorial from YouTube on SpotifyAPI calls (https://www.youtube.com/watch?v=WAmEZBEeNmg&ab_channel=AkamaiDeveloper)
from datetime import datetime

import requests
import base64
import urllib.parse
from flask import Flask, redirect, request, jsonify, session

import gui

from dotenv import load_dotenv
import json
import os

from requests import post, get

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

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
Spotify user authentication
"""
# followed tutorial by Imdad Codes https://www.youtube.com/watch?v=olY_2MW4Eik&t=90s
app = Flask(__name__)
app.secret_key = client_secret

@app.route('/')
def index():
    return "Welcome to NewToMyEars <a href='/login'>Login with Spotify</a>"

@app.route('/login')
def login():
    scope = 'playlist-modify-private'
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': redirect_uri,
        'show_dialog': True
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({'error': request.args['error']})

    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
        }

        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

        return redirect('/playlists')

    @app.route('/playlists')
    def make_playlist():
        if 'access_token' not in session:
            return redirect('/login')

        if datetime.now().timestamp() > session['expires_at']:
            return redirect('/refresh-token')

        headers = {
            'Authorization': f"Bearer {session['access_token']}",
            'Content-Type': 'application/json'
        }

        data = {
            "name": "NewToMyEars",
            "description": "A playlist of 20 unpopular Spotify songs",
            "public": False,
        }

        response = requests.get(API_BASE_URL + 'me/playlists', headers=headers, data=data)
        new_playlist = response.json()
        return jsonify(new_playlist)

    @app.route('/refresh-token')
    def refresh_token():
        if 'refresh_token' not in session:
            return redirect('/login')

        if datetime.now().timestamp() > session['expires_at']:
            req_body = {
                'grant_type': 'refresh_token',
                'refresh_token': session['refresh_token'],
                'client_id': client_id,
                'client_secret': client_secret
            }

            response = requests.post(TOKEN_URL, data=req_body)
            new_token_info = response.json()

            session['access_token'] = new_token_info['access_token']
            session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

            return redirect('/playlists')

app.run(host='0.0.0.0', debug=True)

token = getToken()
genre = input("Genre to explore: ")
result = []
for i in range(0,15):
    result += getPlaylistsofGenre(token, genre, i*35)

songs = getSongsofPlaylists(result)
# print(len(result))
# print(len(songs))
# for song in songs:
#     print(song[0], song[1])