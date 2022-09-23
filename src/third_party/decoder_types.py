import compatibility

if compatibility.running_as_cpython:
    from typing import NewType
    from typing import Callable
    RGBColour = NewType("RGBColour", int)
    PixelRenderer = Callable[[int, int, RGBColour], None]
    XYP = tuple[int, int, int] # type: ignore
else:
    RGBColour = int # type: ignore
    PixelRenderer = callable # type: ignore
    XYP = 'tuple[int, int, int]' # type: ignore


FilePath = str
