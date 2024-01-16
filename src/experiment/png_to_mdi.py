import struct
from typing import Generator, cast
from PIL import Image


class Palette:
    _palette: dict[tuple[int, int, int], int] = {}
    _index: int = 0

    def store_colour_if_new_and_get_index(self, r: int, g: int, b: int) -> int:
        if (r, g, b) not in self._palette:
            self._palette[r, g, b] = self._index
            self._index += 1

        return self._palette[r, g, b]

    @property
    def palette_count(self):
        return len(self._palette)

    @property
    def palette_ordered_colours(self) -> Generator[tuple[int, int, int], None, None]:
        for (key, _) in sorted(self._palette.items(), key=lambda x: x[1]):
            yield key


def int16_bytes(x: int) -> tuple[int, int]:
    return x >> 8, x & 255


image = Image.open("images/matrix-display/matrix-display-coloured.png").convert('RGB')
pixels: list[int] = []
palette = Palette()

for y in range(image.height):
    for x in range(image.width):
        r, g, b = cast(tuple[int, int, int], image.getpixel((x, y)))  # type: ignore
        pixels.append(palette.store_colour_if_new_and_get_index(r, g, b))

mdi_data = struct.pack(">H", palette.palette_count)
for r, g, b in palette.palette_ordered_colours:
    mdi_data += struct.pack("3B", r, g, b)

if palette.palette_count < 256:
    mdi_data += struct.pack("B" * len(pixels), *pixels)
else:
    mdi_data += struct.pack(">H" * len(pixels), *pixels)

with open("images/matrix-display/matrix-display-coloured.mdi", "wb") as mdi_file:
    mdi_file.write(mdi_data)

