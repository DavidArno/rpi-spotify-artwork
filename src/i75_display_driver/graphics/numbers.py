_NUMBERS_5x9 = [
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
        0b10010,
        0b10010,
        0b10010,
        0b10010,
        0b11111,
        0b10010,
        0b10010,
        0b10010,
        0b10010
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

def get_coloured_digit_image_data(digit, background_colour, foreground_colour):
    image_data = []
    for row in _NUMBERS_5x9[digit]:
        image_row_colours = []
        for column_mask in [0b10000, 0b01000, 0b00100, 0b00010, 0b00001]:
            image_row_colours.append(foreground_colour if row & column_mask else background_colour)

        image_data.append(image_row_colours)

    return image_data