import hub75

BLACK = hub75.color(0, 0, 0)
DARK_GREY = hub75.color(64, 64, 64)
MID_GREY = hub75.color(128, 128, 128)
LIGHT_GREY = hub75.color(192, 192, 192)
PROGRESS_ILLUMINATED = hub75.color(141, 98, 178)

def rbg_colour_to_hub75_colour(this, rgb):
    (red, green, blue) = (rgb >> 16) & 0xFF, (rgb >> 8) & 0xFF, rgb & 0xFF
    return hub75.color(red, blue, green)
