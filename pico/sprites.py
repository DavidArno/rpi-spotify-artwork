from typing import Callable

_TICK_DATA = [
    0b00001,
    0b00010,
    0b10100,
    0b01000,
    0b00000
]

_CROSS_DATA = [
    0b00000,
    0b01010,
    0b00100,
    0b01010,
    0b00000
]

_DOT_DATA = [
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b01000
]

_COLON_DATA = [
    0b00000,
    0b00000,
    0b01000,
    0b00000,
    0b01000
]

_QUESTION_MARK_DATA = [
    0b01110,
    0b00001,
    0b00110,
    0b00000,
    0b00100
]

_LETTERS_DATA = [
    [
        0b01110,
        0b10001,
        0b11111,
        0b10001,
        0b10001
    ],
    [
        0b11110,
        0b10001,
        0b11110,
        0b10001,
        0b11110
    ],
    [
        0b01110,
        0b10001,
        0b10000,
        0b10001,
        0b01110
    ],
    [
        0b11110,
        0b10001,
        0b10001,
        0b10001,
        0b11110
    ],
    [
        0b11111,
        0b10000,
        0b11111,
        0b10000,
        0b11111
    ],
    [
        0b11111,
        0b10000,
        0b11111,
        0b10000,
        0b10000
    ],
    [
        0b01110,
        0b10000,
        0b10011,
        0b10001,
        0b01110
    ],
    [
        0b10001,
        0b10001,
        0b11111,
        0b10001,
        0b10001
    ],
    [
        0b01110,
        0b00100,
        0b00100,
        0b00100,
        0b01110
    ],
    [
        0b00111,
        0b00001,
        0b00001,
        0b10001,
        0b01110
    ],
    [
        0b10001,
        0b10010,
        0b11100,
        0b10010,
        0b10001
    ],
    [
        0b10000,
        0b10000,
        0b10000,
        0b10000,
        0b11111
    ],
    [
        0b11011,
        0b10101,
        0b10101,
        0b10001,
        0b10001
    ],
    [
        0b10001,
        0b11001,
        0b10101,
        0b10011,
        0b10001
    ],
    [
        0b01110,
        0b10001,
        0b10001,
        0b10001,
        0b01110
    ],
    [
        0b11110,
        0b10001,
        0b11110,
        0b10000,
        0b10000
    ],
    [
        0b01110,
        0b10001,
        0b10101,
        0b10011,
        0b01110
    ],
    [
        0b11110,
        0b10001,
        0b11110,
        0b10001,
        0b10001
    ],
    [
        0b01110,
        0b10000,
        0b01110,
        0b00001,
        0b11110
    ],
    [
        0b11111,
        0b00100,
        0b00100,
        0b00100,
        0b00100
    ],
    [
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b01110
    ],
    [
        0b10001,
        0b10001,
        0b10001,
        0b01010,
        0b00100
    ],
    [
        0b10001,
        0b10001,
        0b10101,
        0b10101,
        0b01010
    ],
    [
        0b10001,
        0b01010,
        0b00100,
        0b01010,
        0b10001
    ],
    [
        0b10001,
        0b01010,
        0b00100,
        0b00100,
        0b00100        
    ],
    [
        0b11111,
        0b00001,
        0b01110,
        0b10000,
        0b11111
    ]
]

_LOWER_LETTERS_DATA = [
    [
        0b01110,
        0b00001,
        0b01111,
        0b10001,
        0b01111
    ],
    [
        0b10000,
        0b10000,
        0b11110,
        0b10001,
        0b11110
    ],
    [
        0b00000,
        0b01110,
        0b10000,
        0b10000,
        0b01110
    ],
    [
        0b00001,
        0b00001,
        0b01111,
        0b10001,
        0b01111
    ],
    [
        0b01110,
        0b10001,
        0b11111,
        0b10000,
        0b01111
    ],
    [
        0b00111,
        0b01000,
        0b01110,
        0b01000,
        0b01000
    ],
    [
        0b01110,
        0b10001,
        0b01111,
        0b00001,
        0b01111
    ],
    [
        0b10000,
        0b10000,
        0b11110,
        0b10001,
        0b10001
    ],
    [
        0b01000,
        0b00000,
        0b01000,
        0b01000,
        0b01000
    ],
    [
        0b00010,
        0b00000,
        0b00010,
        0b10010,
        0b01100
    ],
    [
        0b10000,
        0b10000,
        0b10100,
        0b11000,
        0b10100
    ],
    [
        0b10000,
        0b10000,
        0b10000,
        0b10010,
        0b01100
    ],
    [
        0b00000,
        0b01010,
        0b10101,
        0b10001,
        0b10001
    ],
    [
        0b00000,
        0b11110,
        0b10001,
        0b10001,
        0b10001
    ],
    [
        0b00000,
        0b01110,
        0b10001,
        0b10001,
        0b01110
    ],
    [
        0b00000,
        0b11110,
        0b10001,
        0b11110,
        0b10000
    ],
    [
        0b00000,
        0b01111,
        0b10001,
        0b01111,
        0b00001
    ],
    [
        0b00000,
        0b10110,
        0b11000,
        0b10000,
        0b10000
    ],
    [
        0b00110,
        0b01000,
        0b00100,
        0b00010,
        0b01100
    ],
    [
        0b01000,
        0b01000,
        0b11110,
        0b01000,
        0b00111
    ],
    [
        0b00000,
        0b10001,
        0b10001,
        0b10011,
        0b01101
    ],
    [
        0b00000,
        0b10001,
        0b01010,
        0b01010,
        0b00100
    ],
    [
        0b00000,
        0b10001,
        0b10001,
        0b10101,
        0b01010
    ],
    [
        0b00000,
        0b10010,
        0b01100,
        0b01100,
        0b10010,
    ],
    [
        0b10001,
        0b10001,
        0b01111,
        0b00001,
        0b01110        
    ],
    [
        0b11110,
        0b00100,
        0b01000,
        0b10000,
        0b11110
    ]
]
        
_NUMBERS_DATA = [
    [
        0b01110,
        0b10011,
        0b10101,
        0b11001,
        0b01110
    ],
    [
        0b00100,
        0b01100,
        0b00100,
        0b00100,
        0b01110
    ],
    [
        0b01110,
        0b10001,
        0b00110,
        0b01000,
        0b11111
    ],
    [
        0b01110,
        0b00001,
        0b01110,
        0b00001,
        0b01110
    ],
    [
        0b10000,
        0b10100,
        0b11110,
        0b00100,
        0b00100
    ],
    [
        0b11110,
        0b10000,
        0b11110,
        0b00001,
        0b11110
    ],
    [
        0b01110,
        0b10000,
        0b11110,
        0b10001,
        0b01110
    ],
    [
        0b11110,
        0b00010,
        0b00100,
        0b01000,
        0b01000
    ],
    [
        0b01110,
        0b10001,
        0b01110,
        0b10001,
        0b01110
    ],
    [
        0b01110,
        0b10001,
        0b01111,
        0b00001,
        0b01110
    ]
]

_SMALL_NUMBERS_DATA = [
    [
        0b111,
        0b101,
        0b101,
        0b101,
        0b111
    ],
    [
        0b010,
        0b110,
        0b010,
        0b010,
        0b111
    ],
    [
        0b111,
        0b001,
        0b111,
        0b100,
        0b111
    ],
    [
        0b111,
        0b001,
        0b111,
        0b001,
        0b111
    ],
    [
        0b100,
        0b101,
        0b111,
        0b001,
        0b001
    ],
    [
        0b111,
        0b100,
        0b111,
        0b001,
        0b111
    ],
    [
        0b111,
        0b101,
        0b101,
        0b101,
        0b111
    ],
    [
        0b111,
        0b001,
        0b001,
        0b010,
        0b010
    ],
    [
        0b111,
        0b101,
        0b111,
        0b101,
        0b111
    ],
    [
        0b111,
        0b101,
        0b111,
        0b001,
        0b111
    ],
]

_SMALL_DOT_DATA = [ 0, 0, 0, 0, 1 ]

_SMALL_QUESTION_MARK_DATA = [
    0b111,
    0b001,
    0b010,
    0b000,
    0b010
]

def _draw_sprite(
    sprite: list[int],
    x: int,
    y: int,
    set_pixel: CallableCallable[[int, int, int, int, int], None],
    width: int,
    red: int,
    green: int,
    blue: int
) -> None:
    for row in range(5):
        for column in range(width):
            mask = 2**((width -1) - column)
            r, g, b = (red, green, blue) if sprite[row] & mask else (0, 0, 0)
            set_pixel(x + column, y + row, r, g, b)
        
def draw_tick(
    x: int,
    y: int,
    set_pixel: CallableCallable[[int, int, int, int, int], None],
    red: int,
    green: int,
    blue: int
) -> None:
    _draw_sprite(_TICK_DATA, x, y, set_pixel, 5, red, green, blue)

def draw_cross(
    x: int,
    y: int,
    set_pixel: CallableCallable[[int, int, int, int, int], None],
    red: int,
    green: int,
    blue: int
) -> None:
    _draw_sprite(_CROSS_DATA, x, y, set_pixel, 5, red, green, blue)
    
def draw_text(
    x: int,
    y: int,
    text: str,
    set_pixel: CallableCallable[[int, int, int, int, int], None],
    red: int,
    green: int,
    blue: int
) -> None:
    x_pos = x
    for c in text:
        i = ord(c)
        if 48 <= i <= 57:
            sprite = _NUMBERS_DATA[i-48]
        elif 65 <= i <= 90:
            sprite = _LETTERS_DATA[i-65]
        elif 97 <= i <= 122:
            sprite = _LOWER_LETTERS_DATA[i-97]
        elif i == 46:
            sprite = _DOT_DATA
        elif i == 58:
            sprite = _COLON_DATA
        elif i == 32:
            x_pos += 6
            continue
        else:
            sprite = _QUESTION_MARK_DATA
        
        _draw_sprite(sprite, x_pos, y, set_pixel, 5, red, green, blue)
        x_pos += 6

def draw_ip_address(
    x: int,
    y: int,
    ip_data: str,
    set_pixel: CallableCallable[[int, int, int, int, int], None],
    red: int,
    green: int,
    blue: int
) -> None:
    x_pos = x
    for c in ip_data:
        i = ord(c)
        if 48 <= i <= 57:
            sprite = _SMALL_NUMBERS_DATA[i-48]
            width = 3
        elif i == 46:
            sprite = _SMALL_DOT_DATA
            width = 1
        else:
            sprite = _SMALL_QUESTION_MARK_DATA
            width = 3
            
        _draw_sprite(sprite, x_pos, y, set_pixel, width, red, green, blue)
        x_pos += width + 1
    
def draw_rectangle(
    x: int,
    y: int,
    width: int,
    height: int,
    set_pixel: CallableCallable[[int, int, int, int, int], None],
    red: int,
    green: int,
    blue: int
) -> None:
    for offset_y in range(height):
        for offset_x in range(width):
            set_pixel(x + offset_x, y + offset_y, red, green, blue)
            