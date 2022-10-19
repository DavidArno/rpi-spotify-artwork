from typing import NamedTuple, NewType

RGBColour = NewType("RGBColour", int)
RGB = NamedTuple('RGB', [('r', int), ('g', int), ('b', int)])

def rgb_colour_to_rgb(rgb:RGBColour) -> RGB:
    return RGB((rgb >> 16) & 0xFF, (rgb >> 8) & 0xFF, rgb & 0xFF)

def rgb_values_to_rgb_colour(r:int, g:int, b:int) -> RGBColour:
    return RGBColour((r << 16) + (g << 8) + b)

def rgb_to_rgb_colour(rgb:RGB) -> RGBColour:
    return RGBColour((rgb.r << 16) + (rgb.g << 8) + rgb.b)

BLACK:RGBColour = rgb_values_to_rgb_colour(0, 0, 0)
WHITE:RGBColour = rgb_values_to_rgb_colour(255, 255, 255)
RED:RGBColour = rgb_values_to_rgb_colour(255, 0, 0)
GREEN:RGBColour = rgb_values_to_rgb_colour(0, 255, 0)
TIME_COLOUR:RGBColour = rgb_values_to_rgb_colour(0, 106, 255)