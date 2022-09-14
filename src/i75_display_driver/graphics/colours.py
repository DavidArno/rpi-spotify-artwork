################################################################################
# Conventions used here for colours:
# rbg          - an (r, g, b) tuple, where each of r, g and b are 0 - 255
# packed_rgb   - an int of form 0x00RRGGBB, where RR, GG and BB are 0x00 - 0xFF
# hub75_colour - gamma corrected (packed_rgb format, I think) int value
################################################################################
import hub75 # type: ignore

BLACK = hub75.color(0, 0, 0)
DARK_GREY = hub75.color(64, 64, 64)
MID_GREY = hub75.color(128, 128, 128)
LIGHT_GREY = hub75.color(192, 192, 192)
PROGRESS_ILLUMINATED = hub75.color(141, 98, 178)

def packed_rgb_to_rgb(rgb):
    return (rgb >> 16) & 0xFF, (rgb >> 8) & 0xFF, rgb & 0xFF

def rgb_to_packed_rgb(r, g, b):
    return (r << 16) + (g << 8) + b
    
def packed_rgb_to_hub75_colour(packed_rgb):
    (r, g, b) = packed_rgb_to_rgb(packed_rgb)
    return hub75.color(r, g, b)
    
def rgb_to_hub75_colour(r, g, b):
    return hub75.color(r, g, b)
