from redblack import RedBlackTree
import base64
from dotenv import load_dotenv
import json
import os
from requests import post, get
import random

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

def getSongsofPlaylists(playlists, rb_tree):
    token = getToken()
    for item in playlists:
        if item is None:
            continue
        playlist_id = item["id"]
        playlist_tracks = getPlaylistSongs(token, playlist_id)
        for tracks in playlist_tracks:
            try:
                name = tracks["track"]["name"]  # Song name
                popularity = tracks["track"]["popularity"]  # Popularity score
            except:
                continue  # Skip if track data is null or incomplete
            # Insert the song into the Red-Black Tree
            rb_tree.insert(popularity, name)

# Initialize the Red-Black Tree
rb_tree = RedBlackTree()

# Fetch playlists and songs
token = getToken()
genre = input("Genre to explore: ")
result = []
for i in range(0, 15):  # Fetch 15 batches of playlists
    result += getPlaylistsofGenre(token, genre, i * 35)


def get_random_song_from_tree(rb_tree, key, song_list):
    # Search for the key in the Red-Black Tree
    song_set = rb_tree.search(key)

    # If the key exists and has songs, choose one randomly
    if song_set:
        random_song = random.choice(list(song_set))  # Convert set to list for random.choice
        song_list.append(random_song)  # Add the song to the list

    else:
        if (key < 99):
            get_random_song_from_tree(rb_tree, key+1, song_list)    # If key does not exist, try again


# Store songs in the Red-Black Tree
getSongsofPlaylists(result, rb_tree)


random_songs = []

# range 1
num_range1_1 = random.randint(1, 10);
num_range1_2 = random.randint(1, 10);

get_random_song_from_tree(rb_tree, num_range1_1, random_songs)
get_random_song_from_tree(rb_tree, num_range1_2, random_songs)


# range 2
num_range2_1 = random.randint(11, 20);
num_range2_2 = random.randint(11, 20);


get_random_song_from_tree(rb_tree, num_range1_1, random_songs)
get_random_song_from_tree(rb_tree, num_range1_2, random_songs)


# range 3

num_range3_1 = random.randint(21, 30);
num_range3_2 = random.randint(21, 30);

get_random_song_from_tree(rb_tree, num_range3_1, random_songs)
get_random_song_from_tree(rb_tree, num_range3_2, random_songs)


# range 4
num_range4_1 = random.randint(31, 40);
num_range4_2 = random.randint(31, 40);

get_random_song_from_tree(rb_tree, num_range4_1, random_songs)
get_random_song_from_tree(rb_tree, num_range4_2, random_songs)


# range 5
num_range5_1 = random.randint(41, 50);
num_range5_2 = random.randint(41, 50);

get_random_song_from_tree(rb_tree, num_range5_1, random_songs)
get_random_song_from_tree(rb_tree, num_range5_2, random_songs)


# Print the final list of random songs
print(f"List of random songs: {random_songs}")

