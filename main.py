from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date_and_year = input("Which year do you want to travel to? Type the date in this formate YYY-MM-DD: ")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date_and_year + "/")
billboard_page = response.text
soup = BeautifulSoup(billboard_page, "html.parser")
song_titles = soup.select(selector="div li h3#title-of-a-story") #Scraping all h3 with song titles
song_list = [title.getText().strip() for title in song_titles]
artists = soup.select(selector="div li.lrv-u-width-100p span")
artist_list = [artist.getText().strip() for artist in artists if not artist.getText().strip().isdigit() if "-" not in artist.getText().strip()]

SPOTIPY_CLIENT_ID = "3b45e04ca5a245d8bef2502b76da4323"
SPOTIPY_CLIENT_SECRET = "ad278a456b1944f08c1610b4356d63e5"
REDIRECT_URI = "https://example.com/callback/"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URI,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]
print(user_id)

song_uris = []
year = date_and_year.split("-")[0]
for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date_and_year} Billboard 100", public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)