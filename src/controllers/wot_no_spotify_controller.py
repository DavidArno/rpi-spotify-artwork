from typing import Callable
from graphics.colours import BLACK, TIME_COLOUR
from graphics.canvas import Canvas, Layer
from graphics.sprites import create_sprite_from_image
from PIL import Image #type: ignore

class WotNoSpotifyController():
    def __init__(self, canvas:Canvas, check_enabled:Callable[[], bool]):
        self._canvas = canvas
        self._check_enabled = check_enabled
        self._draw_bottom_layer()

    def actively_displaying(self, current_time:float) -> bool:
        if not self._check_enabled(): return False

        self._canvas.draw_time(37, 3, TIME_COLOUR, current_time)
        return True

    def _draw_bottom_layer(self):
        image = Image.open('images/wot_no_spotify/bottom_layer.png').convert('RGB')
        sprite = create_sprite_from_image(image)
        self._canvas.draw_sprite(0, 0, sprite, layer = Layer.Bottom)

    def _draw_double_digit(self, x:int, y:int, *, number:int) -> None:
        self._canvas.draw_leading_zero_digits(x, y, TIME_COLOUR, digit_width = 2, number = number, layer = Layer.Top)

    def _draw_seconds_line(self, seconds:int) -> None:
        self._canvas.draw_horizontal_line(2, 0, 60, BLACK, layer = Layer.Top)
        self._canvas.draw_horizontal_line(2, 0, seconds, TIME_COLOUR, layer = Layer.Top)
