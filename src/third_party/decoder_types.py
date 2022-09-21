from typing import NewType
from typing import Callable

FilePath = str
RGBColour = NewType("RGBColour", int)
PixelRenderer = Callable[[int, int, RGBColour], None]
XYP = tuple[int, int, int]
