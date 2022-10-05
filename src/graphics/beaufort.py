################################################################################
# The colours used here are taken from the Beaufort scale colours at
# https://en.wikipedia.org/wiki/Beaufort_scale
################################################################################
from graphics.colours import RGBColour

BeaufortList = list[tuple[RGBColour, int]]

_BEAUFORT_COLOURS:BeaufortList = [
    (RGBColour(0xFFFFFF), 0),
    (RGBColour(0xAEF1F9), 3),
    (RGBColour(0x96F7DC), 6),
    (RGBColour(0x96F7B4), 10),
    (RGBColour(0x6FF46F), 16),
    (RGBColour(0x73ED12), 21),
    (RGBColour(0xA4ED12), 27),
    (RGBColour(0xDAED12), 33),
    (RGBColour(0xEDC212), 40),
    (RGBColour(0xED8F12), 47),
    (RGBColour(0xED6312), 55),
    (RGBColour(0xED2912), 63),
    (RGBColour(0xD5102D), -1)
]
      
def get_colour_for_speed(knots:int) -> RGBColour:
    for (colour, threshold) in _BEAUFORT_COLOURS:
        if knots <= threshold:
            return colour

    return _BEAUFORT_COLOURS[-1][0]