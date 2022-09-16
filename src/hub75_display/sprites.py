from typing import NewType
from hub75_display.colours import Hub75Colour, BLACK, WHITE, rgb_colour_to_hub75_colour
from third_party import JPEGdecoder

Sprite = NewType("Sprite", list[ list[ Hub75Colour ]])

def create_sprite_from_bitmap_data(
    bitmap:list[int], 
    *, 
    width:int, 
    bg_colour:Hub75Colour = BLACK,
    fg_colour:Hub75Colour = WHITE
) -> Sprite:
    sprite = Sprite([])
    for bitmap_row in bitmap:
        row = []
        for column in range(width-1, -1, -1):
            mask = 2**column
            row.append(fg_colour if bitmap_row & mask else bg_colour)

        sprite.append(row)
    
    return sprite

def create_sprite_from_jpeg_data(data:bytes) -> Sprite:
    sprite = Sprite([])

    def build_sprite(sprite:Sprite, x:int, y:int, rgbColour:JPEGdecoder.RGBColour):
        while y >= len(sprite):
            sprite.append([])

        row = sprite[y]
        while x > len(row):
            row.append(BLACK)
        
        row.append(rgb_colour_to_hub75_colour(rgbColour))

    JPEGdecoder.jpeg(
        data, 
        lambda x, y, rgbColour: build_sprite(sprite, x, y, rgbColour).render(64, 64)
    )

    return sprite