import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint


spotify_client_id = "543e82c6cd274a75b300a411daa2690c"
spotify_client_secret = "f2f200c9a1994c07bfa7a2bfc7eefd04"
SPOTIPY_REDIRECT_URI = "http://example.com"


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                                            scope = "user-library-read",
                                            client_id=spotify_client_id, 
                                            client_secret=spotify_client_secret,
                                            redirect_uri=SPOTIPY_REDIRECT_URI))
# travel = input("Type the date you want to travel to (in the last 20 years) in this format YYYY-MM-DD: ")

# response = requests.get(f"https://www.billboard.com/charts/hot-100/{travel}")
response = requests.get(f"https://www.billboard.com/charts/hot-100/2004-10-31")
billboard_page = response.text
soup = BeautifulSoup(billboard_page, 'html.parser')

titles = soup.select(selector="li ul li h3")
title_list = [title.getText().strip("\t\n") for title in titles]
# for title in title_list:
#     print(title)
user_id = sp.current_user()['id']

results = []
r = sp.search(q="U Saved Me", type='track', limit=1)['tracks']['items'][0]['id']
# print(r['tracks']['items'][0]['id'])
# print(r)
for title in title_list:
    results.append(sp.search(q=title, type='track', limit=1)['tracks']['items'][0]['id'])

print(results)

# new_playlist = sp.user_playlist_create(user=user_id,
#                                        name="fTop Songs on {travel}",
#                                        public=True,
#                                        description="The top 100 songs for you from the date you entered")
# add_tracks = sp.user_playlist_add_tracks(user=user_id,
#                                          playlist_id=new_playlist['id'],
#                                          tracks=results,
#                                          )