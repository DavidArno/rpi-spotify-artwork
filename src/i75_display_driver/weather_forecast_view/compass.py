################################################################################
# Set of wind direction arrows.
# Order is (from 0 - 7): ↑ ↗ → ↘ ↓ ↙ ← ↖
################################################################################
from hub75_display.colours import Hub75Colour
from hub75_display.sprites import Sprite, create_sprite_from_bitmap_data

_COMPASS_IMAGE_DATA = [
    [
        0b0001000,
        0b0011100,
        0b0101010,
        0b0001000,
        0b0001000,
        0b0001000,
        0b0001000
    ],
    [
        0b0000111,
        0b0000011,
        0b0000101,
        0b0001000,
        0b0010000,
        0b0100000,
        0b1000000
    ],
    [
        0b0000000,
        0b0000100,
        0b0000010,
        0b1111111,
        0b0000010,
        0b0000100,
        0b0000000
    ],
    [
        0b1000000,
        0b0100000,
        0b0010000,
        0b0001000,
        0b0000101,
        0b0000011,
        0b0000111
    ],
    [
        0b0001000,
        0b0001000,
        0b0001000,
        0b0001000,
        0b0001000,
        0b0101010,
        0b0011100,
        0b0001000
    ],
    [
        0b0000001,
        0b0000010,
        0b0000100,
        0b0001000,
        0b1010000,
        0b1100000,
        0b1110000
    ],
    [
        0b0000000,
        0b0010000,
        0b0100000,
        0b1111111,
        0b0100000,
        0b0010000,
        0b0000000
    ],
    [
        0b1110000,
        0b1100000,
        0b1010000,
        0b0001000,
        0b0000100,
        0b0000010,
        0b0000001
    ]
]

def get_coloured_compass_image_data(
    position:int, 
    background_colour:Hub75Colour, 
    foreground_colour:Hub75Colour
) -> Sprite:
    return create_sprite_from_bitmap_data(
        _COMPASS_IMAGE_DATA[position], 
        width=7, 
        fg_colour=foreground_colour, 
        bg_colour=background_colour
    )
    