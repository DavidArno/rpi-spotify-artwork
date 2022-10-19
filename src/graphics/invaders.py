from graphics.colours import RGBColour
from graphics.sprites import Sprite, create_sprite_from_bitmap_data

_INVADER_IMAGE_DATA = [
    [
        0b100001,
        0b111111,
        0b110011,
        0b011110,
        0b010010,
        0b100001
    ],
    [
        0b000000,
        0b011110,
        0b110011,
        0b111111,
        0b110011,
        0b010010
    ],
    [
        0b001100,
        0b011110,
        0b101101,
        0b010010,
        0b001100,
        0b010010
    ],
    [
        0b001100,
        0b011110,
        0b101101,
        0b011110,
        0b100001,
        0b010010
    ],
    [
        0b011110,
        0b111111,
        0b101101,
        0b111111,
        0b010010,
        0b001100
    ],
    [
        0b011110,
        0b111111,
        0b101101,
        0b111111,
        0b010010,
        0b100001
    ]
]

SAUCER_IMAGE_DATE = [
    0b0011111100,
    0b0111111110,
    0b1010110101,
    0b1111111111,
    0b0100000010
]

INVADER_MISSILE = [
    0b10, 0b01, 0b10, 0b01
]

MISSILE_LAUNCHER = [
    0b00100,
    0b11111,
    0b11111
]

DEFENCE_TOWER = [
    0b0011111100,
    0b0111111110,
    0b1111111111,
    0b1111111111,
    0b1111111111,
    0b1111001111,
    0b1110000111,
    0b1100000011,
    0b1100000011,
    0b1100000011
]


def get_coloured_alien_sprite(
    alien_index:int, 
    background_colour:RGBColour, 
    foreground_colour:RGBColour
) -> Sprite:
    return create_sprite_from_bitmap_data(
        _INVADER_IMAGE_DATA[alien_index], 
        width=6, 
        fg_colour=foreground_colour, 
        bg_colour=background_colour
    )
