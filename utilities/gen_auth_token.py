# You need to create a spotify app and then set up three environment variables 
# with the client ID, client secret and redirect URI:
# 
# SPOTIPY_CLIENT_ID
# SPOTIPY_CLIENT_SECRET
# SPOTIPY_REDIRECT_URI
#
# This script just assumes these are set up and doesn't check first.
# 
# Instructions: run this script and follow the instructions re copy/pasting the 
# URL in the browser into the cmdline prompt. At that stage, you'll have a 
# .cache file in your home directory. Copy that to the home directory of the
# raspberry pi that will run the actual rpi-spotify-artwork code.
#
# Initial tests suggest that the .cache file needs to be in the directory that
# the code is run from. Need to look into that more.

# type: ignore
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-currently-playing"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
spot = sp.currently_playing()

print(spot)

