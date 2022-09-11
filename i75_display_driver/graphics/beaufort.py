################################################################################
# The colours used here are taken from the Beaufort scale colours at
# https://en.wikipedia.org/wiki/Beaufort_scale
################################################################################
import hub75

_BEAUFORT_COLOURS = [
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
    (0xD5102D, 9999)
]

_converted_colours:list|None = None

def _generate_converted_colours():
    converted_colours = []
    for (colour, knots) in _BEAUFORT_COLOURS:
        (red, green, blue) = (colour >> 16) & 0xFF, (colour >> 8) & 0xFF, colour & 0xFF
        converted_colours.append(hub75.color(red, blue, green), knots)

def get_colour_for_speed(knots):
    if _converted_colours is None:
        _converted_colours = _generate_converted_colours()

    for (colour, threshold) in _converted_colours:
        if knots <= threshold:
            return colour