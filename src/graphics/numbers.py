from common.graphics.sprites import Sprite, create_sprite_from_bitmap_data
from common.graphics.colours import RGBColour

_NUMBERS_5x9: list[list[int]] = [
    [               # 0
        0b01110,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b01110
    ],
    [               # 1 etc
        0b00010,
        0b00110,
        0b00010,
        0b00010,
        0b00010,
        0b00010,
        0b00010,
        0b00010,
        0b00111
    ],
    [
        0b01110,
        0b10001,
        0b00001,
        0b00001,
        0b00010,
        0b00100,
        0b01000,
        0b10000,
        0b11111
    ],
    [
        0b01110,
        0b10001,
        0b00001,
        0b00001,
        0b00110,
        0b00001,
        0b00001,
        0b10001,
        0b01110
    ],
    [
        0b10000,
        0b10000,
        0b10010,
        0b10010,
        0b10010,
        0b11111,
        0b00010,
        0b00010,
        0b00010
    ],
    [
        0b11111,
        0b10000,
        0b10000,
        0b10000,
        0b11110,
        0b00001,
        0b00001,
        0b00001,
        0b11110
    ],
    [
        0b00110,
        0b01000,
        0b10000,
        0b10000,
        0b11110,
        0b10001,
        0b10001,
        0b10001,
        0b01110
    ],
    [
        0b11111,
        0b00001,
        0b00001,
        0b00010,
        0b00010,
        0b00100,
        0b00100,
        0b00100,
        0b00100
    ],
    [
        0b01110,
        0b10001,
        0b10001,
        0b10001,
        0b01110,
        0b10001,
        0b10001,
        0b10001,
        0b01110
    ],
    [
        0b01110,
        0b10001,
        0b10001,
        0b10001,
        0b01111,
        0b00001,
        0b00001,
        0b00010,
        0b01100
    ]
]


def get_coloured_digit_sprite(
    digit: int,
    background_colour: RGBColour,
    foreground_colour: RGBColour
) -> Sprite:
    return create_sprite_from_bitmap_data(
        _NUMBERS_5x9[digit],
        width=5,
        fg_colour=foreground_colour,
        bg_colour=background_colour
    )
