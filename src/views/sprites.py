from typing import NewType
from views.colours import RGB
from views.colours import RGBColour, BLACK, WHITE, rgb_to_rgb_colour
from PIL.Image import Image

Sprite = NewType("Sprite", list[ list[ RGBColour ]])

def create_sprite_from_bitmap_data(
    bitmap:list[int], 
    *, 
    width:int, 
    bg_colour:RGBColour = BLACK,
    fg_colour:RGBColour = WHITE
) -> Sprite:
    sprite = Sprite([])
    for bitmap_row in bitmap:
        row = []
        for column in range(width-1, -1, -1):
            mask = 2**column
            row.append(fg_colour if bitmap_row & mask else bg_colour)

        sprite.append(row)
    
    return sprite

def create_sprite_from_image(image:Image) -> Sprite:
    sprite = Sprite([])

    def build_sprite(sprite:Sprite, x:int, y:int, colour:RGBColour):
        while y >= len(sprite):
            sprite.append([])

        row = sprite[y]
        while x > len(row):
            row.append(BLACK)
        
        row.append(colour)

    for y in range(image.height):
        for x in range(image.width):
            r, g, b = image.getpixel((x, y))
            build_sprite(sprite, x, y, rgb_to_rgb_colour(RGB(r, g, b)))

    return sprite