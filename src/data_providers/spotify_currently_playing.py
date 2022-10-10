from typing import Any, Optional
import spotipy #type: ignore
from spotipy.oauth2 import SpotifyOAuth #type: ignore

class SpotifyCurrentlyPlaying:

    def __init__(self):
        self._spotify =  spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-read-currently-playing"))

    def get_current_state(self) -> tuple[bool, Optional[str], int, int, bool]:
        result:Any = self._spotify.currently_playing() #type: ignore
        if result == None:
            return False, None, 0, 0, False

        elapsed_time = result["progress_ms"]
        album_image_url = result["item"]["album"]["images"][2]["url"]
        track_length = result["item"]["duration_ms"]
        paused = not result["is_playing"]
        
        return True, album_image_url, elapsed_time, track_length, paused


