import requests
from asyncio import format_helpers
from views.view import View, Layer
from views.sprites import create_sprite_from_image
from views.colours import RGBColour, rgb_values_to_rgb_colour
from data_providers.spotify_currently_playing import SpotifyCurrentlyPlaying
from PIL import Image
from io import BytesIO

_BLACK:RGBColour = rgb_values_to_rgb_colour(0, 0, 0)
_DARK_GREY:RGBColour = rgb_values_to_rgb_colour(64, 64, 64)
_MID_GREY:RGBColour = rgb_values_to_rgb_colour(128, 128, 128)
_LIGHT_GREY:RGBColour = rgb_values_to_rgb_colour(192, 192, 192)
_PROGRESS_ILLUMINATED:RGBColour = rgb_values_to_rgb_colour(255, 200, 0)
_ACTIVE_REFRESH_DELAY:float = 0.3
_INACTIVE_REFRESH_DELAYS:list[float] = [0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0]

class SpotifyController:
    def __init__(self, view:View, spotify:SpotifyCurrentlyPlaying):
        self._view = view
        self._spotify = spotify
        self._album_image_url = None
        self._draw_progress_container()
        self._inactive_refresh_delay_index:int = -1
        self._inactive_refresh_count:int = 0
        self._last_time:float = 0.0
        self._current_refresh_delay:float = _ACTIVE_REFRESH_DELAY

    def actively_displaying(self, current_time:float) -> bool:
        if current_time >= self._last_time + self._current_refresh_delay:
            active, album_image_url, elapsed_time, track_length, paused = self._spotify.get_current_state()
            if not active:
                if self._inactive_refresh_delay_index == -1:
                    self._inactive_refresh_delay_index = 0
                    self._inactive_refresh_count = 0

                self._inactive_refresh_count += 1
                if self._inactive_refresh_count > 10:
                    self._inactive_refresh_count = 0
                    self._inactive_refresh_delay_index += 1 \
                        if self._inactive_refresh_delay_index < len(_INACTIVE_REFRESH_DELAYS) - 1 \
                        else 0

                self._current_refresh_delay = _INACTIVE_REFRESH_DELAYS[self._inactive_refresh_delay_index]
                print(f"Delaying for {self._current_refresh_delay} seconds")

            else:
                if album_image_url != self._album_image_url:
                    response = requests.get(album_image_url)
                    image = Image.open(BytesIO(response.content)).convert('RGB')
                    sprite = create_sprite_from_image(image)
                    self._view.draw_sprite(0, 0, sprite, layer=Layer.Bottom)
                    self._album_image_url = album_image_url

                if paused:
                    self._pause()
                else:
                    self._resume()

                self._update_progress(elapsed_time, track_length)
                self._current_refresh_delay = _ACTIVE_REFRESH_DELAY
                self._inactive_refresh_delay_index = -1

                print(f"{album_image_url}")
        
            self._last_time = current_time

    def _update_progress(self, so_far_time:int, total_time:int) -> bool:
        width = int(so_far_time / total_time * 50 + 0.5)

        if width > 0:
            self._view.flood_fill(7, 55, width, 3, _PROGRESS_ILLUMINATED, layer = Layer.Top)

        if width < 50:
            self._view.flood_fill(7 + width, 55, 50 - width, 3, _MID_GREY, layer = Layer.Top)
        
    def _draw_progress_container(self) -> None:
        self._draw_indented_rectangle(Layer.Top, 6, 54, 52, 5)

    def _pause(self):
        self._draw_indented_rectangle(Layer.Top, 22, 11, 7, 32)
        self._draw_indented_rectangle(Layer.Top, 35, 11, 7, 32)

    def _resume(self):
        self._view.flood_fill(22, 11, 7, 32, _BLACK, layer = Layer.Top)
        self._view.flood_fill(35, 11, 7, 32, _BLACK, layer = Layer.Top)

    def _draw_indented_rectangle(self, layer:Layer, x:int, y:int, width:int, height:int):
        self._view.draw_horizontal_line(x, y, width-1, _DARK_GREY, layer=layer)
        self._view.draw_vertical_line(x, y+1, height-2, _DARK_GREY, layer=layer)
        self._view.draw_horizontal_line(x+1, y + height - 1, width-1, _LIGHT_GREY, layer=layer)
        self._view.draw_vertical_line(x + width - 1, y+1, height-2, _LIGHT_GREY, layer=layer)
        self._view.set_pixel(x + width - 1, y, _MID_GREY, layer=layer)
        self._view.set_pixel(x, y + height - 1, _MID_GREY, layer=layer)
        self._view.flood_fill(x+1, y+1, width-2, height-2, _MID_GREY, layer=layer)

