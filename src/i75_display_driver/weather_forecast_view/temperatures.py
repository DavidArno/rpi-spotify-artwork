################################################################################
# The colours used here are taken from the css data from 
# https://www.bbc.co.uk/weather and are the colours used by the BBC for their
# weather forecasts. They are used here without permission.
################################################################################
import compatibility

if compatibility.running_as_cpython:
    from typing import Generator
    ColoursGenerator = Generator[tuple[Hub75Colour, int], None, None]  # type: ignore
    ColoursList = list[tuple[int, int]]  # type: ignore
else:
    ColoursList = 'list[tuple[int, int]]'  # type: ignore
    ColoursGenerator = object  # type: ignore

from third_party.decoder_types import RGBColour
from hub75_display.colours import Hub75Colour, rgb_colour_to_hub75_colour

_TEMPERATURE_COLOURS = [
    (0x850100, 40),
    (0x9A1B1E, 36),
    (0xC12026, 30),
    (0xEE2D29, 25),
    (0xEB5038, 21),
    (0xF26A30, 19),
    (0xF68A1F, 17),
    (0xFAA31A, 15),
    (0xFBB616, 13),
    (0xFCC90D, 11),
    (0xFEDB00, 9),
    (0xD0D73E, 7),
    (0xAFD251, 5),
    (0x9FCD80, 3),
    (0xAAD6AE, 1),
    (0xAEDCD8, -2),
    (0x51BFED, -5),
    (0x43A3D9, -10),
    (0x3789C6, -15),
    (0x2374B6, -22),
    (0x0262A9, -99)
]


def _generate_converted_colours(temp_data:ColoursList) -> ColoursGenerator:
    for (colour, temperature) in temp_data:
        yield rgb_colour_to_hub75_colour(RGBColour(colour)), temperature

_converted_colours = [x for x in _generate_converted_colours(_TEMPERATURE_COLOURS)]
        
def get_colour_for_temperature(temperature:int) -> Hub75Colour:
    for (colour, threshold) in _converted_colours:
        if temperature >= threshold:
            return colour

    return _converted_colours[-1][0]