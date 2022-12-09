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

_SAUCER_IMAGE_DATA = [
    0b0011111100,
    0b0111111110,
    0b1010110101,
    0b1111111111,
    0b0100000010
]

_BOMB_IMAGE_DATA = [
    0b10, 0b01, 0b10, 0b01
]

_MISSILE_IMAGE_DATA = [
    0b1, 0b1, 0b1, 0b1
]

_MISSILE_LAUNCHER_IMAGE_DATA = [
    0b00100,
    0b11111,
    0b11111
]

_DEAD_LAUNCHER_IMAGE_DATA = [
    0b0010001,
    0b1100100,
    0b1101010,
    0b0111100
]

_DEFENCE_TOWER_IMAGE_DATA = [
    0b0011111100,
    0b0111111110,
    0b1111111111,
    0b1111001111,
    0b1110000111,
    0b1100000011,
    0b1100000011
]

INVADER_WIDTH = 6
INVADER_HEIGHT = 6
SAUCER_WIDTH = 10
SAUCER_HEIGHT = 5
DEFENCE_TOWER_WIDTH = 10
DEFENCE_TOWER_HEIGHT = 7
BOMB_WIDTH = 2
BOMB_HEIGHT = 4
MISSILE_WIDTH = 1
MISSILE_HEIGHT = 4
MISSILE_LAUNCHER_WIDTH = 5
MISSILE_LAUNCHER_HEIGHT = 3
DEAD_LAUNCHER_WIDTH = 5
DEAD_LAUNCHER_HEIGHT = 3


def get_coloured_invader_sprite(
    invader_index: int,
    background_colour: RGBColour,
    foreground_colour: RGBColour
) -> Sprite:
    return create_sprite_from_bitmap_data(
        _INVADER_IMAGE_DATA[invader_index],
        width=INVADER_WIDTH,
        fg_colour=foreground_colour,
        bg_colour=background_colour
    )


def get_coloured_saucer_sprite(
    background_colour: RGBColour,
    foreground_colour: RGBColour
) -> Sprite:
    return create_sprite_from_bitmap_data(
        _SAUCER_IMAGE_DATA,
        width=SAUCER_WIDTH,
        fg_colour=foreground_colour,
        bg_colour=background_colour
    )


def get_coloured_defence_tower_sprite(
    background_colour: RGBColour,
    foreground_colour: RGBColour
) -> Sprite:
    return create_sprite_from_bitmap_data(
        _DEFENCE_TOWER_IMAGE_DATA,
        width=DEFENCE_TOWER_WIDTH,
        fg_colour=foreground_colour,
        bg_colour=background_colour
    )


def get_coloured_bomb_sprite(
    background_colour: RGBColour,
    foreground_colour: RGBColour
) -> Sprite:
    return create_sprite_from_bitmap_data(
        _BOMB_IMAGE_DATA,
        width=BOMB_WIDTH,
        fg_colour=foreground_colour,
        bg_colour=background_colour
    )


def get_coloured_missile_sprite(
    background_colour: RGBColour,
    foreground_colour: RGBColour
) -> Sprite:
    return create_sprite_from_bitmap_data(
        _MISSILE_IMAGE_DATA,
        width=MISSILE_WIDTH,
        fg_colour=foreground_colour,
        bg_colour=background_colour
    )


def get_coloured_missile_launcher_sprite(
    background_colour: RGBColour,
    foreground_colour: RGBColour
) -> Sprite:
    return create_sprite_from_bitmap_data(
        _MISSILE_LAUNCHER_IMAGE_DATA,
        width=MISSILE_LAUNCHER_WIDTH,
        fg_colour=foreground_colour,
        bg_colour=background_colour
    )


def get_coloured_dead_launcher_sprite(
    background_colour: RGBColour,
    foreground_colour: RGBColour
) -> Sprite:
    return create_sprite_from_bitmap_data(
        _DEAD_LAUNCHER_IMAGE_DATA,
        width=DEAD_LAUNCHER_WIDTH,
        fg_colour=foreground_colour,
        bg_colour=background_colour
    )
