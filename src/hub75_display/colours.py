from typing import NamedTuple, NewType
from third_party.decoder_types import RGBColour
import hub75 # type: ignore

Hub75Colour = NewType("Hub75Colour", int)
RGB = NamedTuple('RGB', [('r', int), ('g', int), ('b', int)])


BLACK:Hub75Colour = hub75.color(0, 0, 0)
WHITE:Hub75Colour = hub75.color(255, 255, 255)

def rgb_colour_to_rgb(rgb:RGBColour) -> RGB:
    return RGB((rgb >> 16) & 0xFF, (rgb >> 8) & 0xFF, rgb & 0xFF)

def rgb_values_to_rgb_colour(r:int, g:int, b:int) -> int:
    return (r << 16) + (g << 8) + b

def rgb_to_rgb_colour(rgb:RGB) -> int:
    return (rgb.r << 16) + (rgb.g << 8) + rgb.b
    
def rgb_colour_to_hub75_colour(rgb_colour:RGBColour) -> Hub75Colour:
    (r, g, b) = rgb_colour_to_rgb(rgb_colour)
    return hub75.color(r, g, b)
    
def rgb_values_to_hub75_colour(r:int, g:int, b:int) -> Hub75Colour:
    return hub75.color(r, g, b)
    
def rgb_to_hub75_colour(rgb:RGB) -> Hub75Colour:
    return hub75.color(rgb.r, rgb.g, rgb.b)
