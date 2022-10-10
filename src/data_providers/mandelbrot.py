################################################################################
# This code is partially borrowed from 
# https://realpython.com/mandelbrot-set-python and is assumed to be copyright
# Real Python or the author, Bartosz Zaczyński. 
################################################################################
from typing import NamedTuple, Generator, Union

_MAX_ITERATIONS = 256
_ESCAPE_RADIUS = 12.0

StabilityPoint = NamedTuple("StabilityPoint", [("x", int), ("y", int), ("stability", float)])

class MandelbrotStabilityGrid():
    def __init__(self, grid_width:int, grid_height:int, centre:complex, width:float):
        self._grid_width = grid_width
        self._grid_height = grid_height
        self._scale = width / 64
        height = self._scale * 64
        #self._centre = centre
        self._offset = centre + complex(-width, height) / 2

    def __iter__(self) -> Generator[StabilityPoint, None, None]:
        for y in range(self._grid_height):
            for x in range(self._grid_width):
                c = self._xy_to_complex(x, y, self._scale, self._offset)
                s = self._stability(c)
                yield StabilityPoint(x, y, s)

    def _xy_to_complex(self, x:int, y:int, scale:float, offset:complex) -> complex:
        return complex(x, -y) * scale + offset

    def _stability(self, c: complex) -> float:
        value = self._escape_count(c, _ESCAPE_RADIUS, _MAX_ITERATIONS) / _MAX_ITERATIONS
        return max(0.0, min(value, 1.0))

    def _escape_count(self, c: complex, escape_radius, max_iterations) -> Union[int, float]:
        z = complex(0)
        for iteration in range(max_iterations):
            z = z**2 + c
            if abs(z) > escape_radius:
                return iteration

        return max_iterations

class MandelbrotSet():

    def __init__(self, width:int, height:int):
        self._grid_width = width
        self._grid_height = height

    def get_stability_grid(self, centre:complex, width:float) -> MandelbrotStabilityGrid:
        return MandelbrotStabilityGrid(self._grid_width, self._grid_height, centre, width)
