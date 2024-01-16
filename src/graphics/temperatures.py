################################################################################
# The colours used here are taken from the css data from
# https://www.bbc.co.uk/weather and are the colours used by the BBC for their
# weather forecasts. They are used here without permission.
################################################################################
from common.graphics.colours import RGBColour

ColoursList = list[tuple[RGBColour, int]]

_TEMPERATURE_COLOURS = [
    (RGBColour(0x850100), 40),
    (RGBColour(0x9A1B1E), 36),
    (RGBColour(0xC12026), 30),
    (RGBColour(0xEE2D29), 25),
    (RGBColour(0xEB5038), 21),
    (RGBColour(0xF26A30), 19),
    (RGBColour(0xF68A1F), 17),
    (RGBColour(0xFAA31A), 15),
    (RGBColour(0xFBB616), 13),
    (RGBColour(0xFCC90D), 11),
    (RGBColour(0xFEDB00), 9),
    (RGBColour(0xD0D73E), 7),
    (RGBColour(0xAFD251), 5),
    (RGBColour(0x9FCD80), 3),
    (RGBColour(0xAAD6AE), 1),
    (RGBColour(0xAEDCD8), -2),
    (RGBColour(0x51BFED), -5),
    (RGBColour(0x43A3D9), -10),
    (RGBColour(0x3789C6), -15),
    (RGBColour(0x2374B6), -22),
    (RGBColour(0x0262A9), -99)
]


def get_colour_for_temperature(temperature: int) -> RGBColour:
    for (colour, threshold) in _TEMPERATURE_COLOURS:
        if temperature >= threshold:
            return colour

    return _TEMPERATURE_COLOURS[-1][0]