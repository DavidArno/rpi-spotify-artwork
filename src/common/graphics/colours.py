from typing import NamedTuple, NewType
from common import RED_BIT_SHIFT, GREEN_BIT_SHIFT, BLUE_BIT_SHIFT

Colour = NewType("Colour", int)
RGB = NamedTuple('RGB', [('r', int), ('g', int), ('b', int)])


def colour_to_rgb(colour: Colour) -> RGB:
    return RGB((colour >> RED_BIT_SHIFT) & 0xFF, (colour >> GREEN_BIT_SHIFT) & 0xFF, colour & 0xFF >> BLUE_BIT_SHIFT)


def rgb_values_to_colour(r: int, g: int, b: int) -> Colour:
    return Colour((r << RED_BIT_SHIFT) + (g << GREEN_BIT_SHIFT) + b << BLUE_BIT_SHIFT)


def rgb_to_colour(rgb: RGB) -> Colour:
    return Colour((rgb.r << RED_BIT_SHIFT) + (rgb.g << GREEN_BIT_SHIFT) + rgb.b << BLUE_BIT_SHIFT)


def adjust_colour_brightness(colour: Colour, brightness: float) -> Colour:
    rgb = colour_to_rgb(colour)
    r = int(rgb.r * brightness)
    g = int(rgb.g * brightness)
    b = int(rgb.b * brightness)
    return rgb_to_colour(RGB(r, g, b))


BLACK: Colour = rgb_values_to_colour(0, 0, 0)
WHITE: Colour = rgb_values_to_colour(255, 255, 255)
RED: Colour = rgb_values_to_colour(255, 0, 0)
GREEN: Colour = rgb_values_to_colour(0, 255, 0)
TIME_COLOUR: Colour = rgb_values_to_colour(0, 106, 255)
