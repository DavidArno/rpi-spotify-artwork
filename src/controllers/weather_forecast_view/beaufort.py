################################################################################
# The colours used here are taken from the Beaufort scale colours at
# https://en.wikipedia.org/wiki/Beaufort_scale
################################################################################
import compatibility

if compatibility.running_as_cpython:
    from typing import Generator
    ColoursGenerator = Generator[tuple[Hub75Colour, int], None, None] # type: ignore
    BeaufortList = list[tuple[int, int]] # type: ignore
else:
    ColoursGenerator = object  # type: ignore
    BeaufortList = 'list[tuple[int, int]]' # type: ignore

from third_party.decoder_types import RGBColour
from hub75_display.colours import Hub75Colour, rgb_colour_to_hub75_colour

_BEAUFORT_COLOURS:BeaufortList = [ # type: ignore
    (0xFFFFFF, 0),
    (0xAEF1F9, 3),
    (0x96F7DC, 6),
    (0x96F7B4, 10),
    (0x6FF46F, 16),
    (0x73ED12, 21),
    (0xA4ED12, 27),
    (0xDAED12, 33),
    (0xEDC212, 40),
    (0xED8F12, 47),
    (0xED6312, 55),
    (0xED2912, 63),
    (0xD5102D, -1)
]

def _generate_converted_colours(beaufort_data:BeaufortList) -> ColoursGenerator:
    for (colour, knots) in beaufort_data:
        yield rgb_colour_to_hub75_colour(RGBColour(colour)), knots

_converted_colours = [x for x in _generate_converted_colours(_BEAUFORT_COLOURS)]
        
def get_colour_for_speed(knots:int) -> Hub75Colour:
    for (colour, threshold) in _converted_colours:
        if knots <= threshold:
            return colour

    return _converted_colours[-1][0]