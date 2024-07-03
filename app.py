import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint
CLIENT_ID = ***CLIENT ID***
CLIENT_SECRET_KEY = ***CLIENT SECRET KEY***
REDIRECT_URI = "http://example.com"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET_KEY, redirect_uri=REDIRECT_URI, scope="playlist-modify-private"))
user_info = sp.current_user()
user_id = user_info['id']

date = str(input("Enter your preferred date in the format(YYYY-MM-DD): "))
URL = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(URL)
response.raise_for_status()
data = response.text
soup = BeautifulSoup(data, "html.parser")
song_titles = []

#getting all the songs from the given date
songs = soup.select('h3.c-title.a-no-trucate.a-font-primary-bold-s.u-letter-spacing-0021')
for song in songs:
    song_name = song.getText()
    title_song = song_name.strip()
    song_titles.append(title_song)


spotify_uris = []
year = date.split('-')[0]
for song in song_titles:
    try:
        search_results = sp.search(q=f"track: {song} year: {year}", type="track")
        tracks = search_results.get("tracks", {}).get("items", [])

        # Check if any tracks were found
        if tracks:
            # Assuming the first result is the desired song
            first_track = tracks[0]
            spotify_uri = first_track["uri"]
            spotify_uris.append(spotify_uri)
            print(f"Found Spotify URI for: {song}")
        else:
            print(f"Song not found on Spotify: {song}")

    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching Spotify data for {song}: {e}")

playlist_name = f"{date} Billboard 100"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
sp.playlist_add_items(playlist['id'], spotify_uris)
