from typing import Callable, NewType, cast
from common import Colour, BLACK, WHITE, rgb_to_colour
#from PIL.Image import Image  # type: ignore

Sprite = NewType("Sprite", list[list[Colour]])


def create_sprite_from_mono_bitmap_(
        bitmap: list[int],
        *,
        width: int,
        bg_colour: Colour = BLACK,
        fg_colour: Colour = WHITE
) -> Sprite:
    sprite = Sprite([])
    for bitmap_row in bitmap:
        row: list[Colour] = []
        for column in range(width - 1, -1, -1):
            mask = 2**column
            row.append(fg_colour if bitmap_row & mask else bg_colour)

        sprite.append(row)

    return sprite


# def create_sprite_from_image(image: Image) -> Sprite:
#     return _create_sprite_from_image_with_recolouring(image, lambda c: c)


# def create_coloured_sprite_from_mono_image(image: Image, *, foreground_colour: RGBColour) -> Sprite:
#     return _create_sprite_from_image_with_recolouring(image, lambda c: BLACK if c == BLACK else foreground_colour)


def _create_sprite_from_image_with_recolouring(image: Image, recolour: Callable[[RGBColour], RGBColour]) -> Sprite:
    sprite = Sprite([])

    def build_sprite(sprite: Sprite, x: int, y: int, colour: RGBColour):
        while y >= len(sprite):
            sprite.append([])

        row = sprite[y]
        while x > len(row):
            row.append(BLACK)

        row.append(colour)

    for y in range(image.height):
        for x in range(image.width):
            r, g, b = cast(tuple[int, int, int], image.getpixel((x, y)))  # type: ignore
            colour = recolour(rgb_to_rgb_colour(RGB(r, g, b)))
            build_sprite(sprite, x, y, colour)

    return sprite