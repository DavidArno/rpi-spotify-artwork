import colorsys
from typing import Callable
from graphics.colours import rgb_values_to_rgb_colour, RGBColour
from data_providers.mandelbrot import MandelbrotSet
from graphics.canvas import Canvas, Layer


class MandelbrotController():
    def __init__(self, canvas:Canvas, mandelbrot_set:MandelbrotSet, check_enabled:Callable[[], bool]):
        self._canvas = canvas
        self._check_enabled = check_enabled
        self._last_time = 0.0
        self._mandelbrot_set = mandelbrot_set
        self._centre = -0.7442 + 0.1314j
        self._width = 3

    def actively_displaying(self, current_time:float) -> bool:
        if not self._check_enabled(): return False

        for point in self._mandelbrot_set.get_stability_grid(self._centre, self._width):
            self._canvas.set_pixel(point.x, point.y, self._stability_colour(point.stability), layer = Layer.Top)

        self._width /= 1.1

        return True

    def _stability_colour(self, stability:float) -> RGBColour:
        r, g, b = (0, 0, 0) if stability == 1 else colorsys.hsv_to_rgb((20 + stability * 360) % 360 / 360, 0.8, 1)
        return rgb_values_to_rgb_colour(int(r * 255), int(g * 255), int(b * 255))


