# Add the project's libraries path to the list searched when import is used
import sys
sys.path.append('/message_handler')

# Now import everything else needed
import micropython
import select
import time
import ubinascii
import hub75

WIDTH = 64
HEIGHT = 64
matrix = hub75.Hub75(WIDTH, HEIGHT, stb_invert=True)
matrix.start()

rgb_sets = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1]]
line = -31
while True:
    time.sleep(0.05)

    for i in range(8):
        rgb = rgb_sets[i]

        for n in range(256):
            y = int(n/64) + 4 * i + line
            if (y >= 0 and y <= 63):
                matrix.set_rgb(n % 64, y, rgb[0] * n, rgb[1] * n, rgb[2] * n)

    line += 1
    if line >= 64:
        line = -31

    matrix.flip()
