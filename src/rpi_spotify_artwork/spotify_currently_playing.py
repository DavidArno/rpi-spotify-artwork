# type: ignore
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image
import requests
from io import StringIO

scope = "user-read-currently-playing"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
current_track = sp.current_user_playing_track()

if current_track is None:
    print("not running, mate.")
else:
    print(current_track["item"]["album"]["images"])
    print(current_track["is_playing"])
    print(current_track["item"]["duration_ms"])
    print(current_track["progress_ms"])

    images = current_track["item"]["album"]["images"]
    if len(images) >= 4 and (required_image := images[3])["height"] == 64: 
        url = required_image["url"]
        response = requests.get(url)
        img = Image.open(StringIO(response.content))

    for i in range(8):
        bit = 2 ** i
        print(bit)