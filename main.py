import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint


spotify_client_id = "543e82c6cd274a75b300a411daa2690c"
spotify_client_secret = "2529c0a00ad647a1be473fe6a9d49bb6"
SPOTIPY_REDIRECT_URI = "http://example.com"


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope = "playlist-modify-private",
        client_id=spotify_client_id, 
        client_secret=spotify_client_secret,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        show_dialog=True,
        cache_path='token.txt'))
# travel = input("Type the date you want to travel to (in the last 20 years) in this format YYYY-MM-DD: ")
# response = requests.get(f"https://www.billboard.com/charts/hot-100/{travel}")

response = requests.get(f"https://www.billboard.com/charts/hot-100/2004-10-31")
billboard_page = response.text
soup = BeautifulSoup(billboard_page, 'html.parser')

titles = soup.select(selector="li ul li h3")
title_list = [title.getText().strip("\t\n") for title in titles]

user_id = sp.current_user()['id']

song_uris = []
r = sp.search(q="U Saved Me", type='track', limit=1)['tracks']['items'][0]['id']

for title in title_list:
    song_uris.append(sp.search(q=title, type='track', limit=1)['tracks']['items'][0]['id'])

# print(song_uris)

new_playlist = sp.user_playlist_create(user=user_id,
                                       name="Top Songs on date",
                                       public=False)
add_tracks = sp.user_playlist_add_tracks(user=user_id,
                                         playlist_id=new_playlist['id'],
                                         tracks=song_uris,
                                         )
# print(new_playlist)