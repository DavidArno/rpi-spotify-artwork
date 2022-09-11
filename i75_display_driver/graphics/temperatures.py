################################################################################
# The colours used here are taken from the css data from 
# https://www.bbc.co.uk/weather and are the colours used by the BBC for their
# weather forecasts. They are used here without permission.
################################################################################

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
    (0x0262A9, -9999)
]

_converted_colours:list|None = None

def _generate_converted_colours():
    converted_colours = []
    for (colour, temp) in _TEMPERATURE_COLOURS:
        (red, green, blue) = (colour >> 16) & 0xFF, (colour >> 8) & 0xFF, colour & 0xFF
        converted_colours.append(hub75.color(red, blue, green), temp)

def get_colour_for_temperature(temperature):
    if _converted_colours is None:
        _converted_colours = _generate_converted_colours()

    for (colour, threshold) in _converted_colours:
        if temperature >= threshold:
            return colour