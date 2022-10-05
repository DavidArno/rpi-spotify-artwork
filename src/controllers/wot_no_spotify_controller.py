import time
from typing import Callable
from graphics.colours import RGBColour, rgb_values_to_rgb_colour, BLACK
from graphics.canvas import Canvas, Layer
from graphics.sprites import create_sprite_from_image
from graphics.numbers import get_coloured_digit_sprite
from PIL import Image

_TIME_COLOUR:RGBColour = rgb_values_to_rgb_colour(0, 106, 255)

class WotNoSpotifyController():
    def __init__(self, canvas:Canvas, check_enabled:Callable[[], bool]):
        self._canvas = canvas
        self._check_enabled = check_enabled
        self._draw_bottom_layer()

    def actively_displaying(self, current_time:float) -> bool:
        if not self._check_enabled(): return False

        timeval = time.localtime(current_time)
        self._draw_double_digit(37, 3, number = timeval.tm_hour)
        self._draw_double_digit(51, 3, number = timeval.tm_min)
        self._draw_seconds_line(s if (s := timeval.tm_sec) > 0 else 60)

    def _draw_bottom_layer(self):
        image = Image.open('images/wot_no_spotify/bottom_layer.png').convert('RGB')
        sprite = create_sprite_from_image(image)
        self._canvas.draw_sprite(0, 0, sprite, layer = Layer.Bottom)

    def _draw_double_digit(self, x:int, y:int, *, number:int) -> None:
        digits = [int(x) for x in f"{number:02d}"]
        for i in range(2):
            sprite = get_coloured_digit_sprite(digits[i], BLACK, _TIME_COLOUR)
            self._canvas.draw_sprite(i * 6 + x, y, sprite, layer = Layer.Top)

    def _draw_seconds_line(self, seconds:int) -> None:
        self._canvas.draw_horizontal_line(2, 0, 60, BLACK, layer = Layer.Top)
        self._canvas.draw_horizontal_line(2, 0, seconds, _TIME_COLOUR, layer = Layer.Top)
