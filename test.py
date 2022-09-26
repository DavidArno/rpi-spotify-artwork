# Add the project's libraries path to the list searched when import is used
import sys
#sys.path.append('/message_')

# Now import everything else needed
import os
import micropython
import select
import time
import ubinascii
import hub75
from third_party import JPEGdecoder

print(sys.platform)

print(os.uname())

if __name__ == "__main__":
    print("Checking __main__ works")
else:
    print(f"__name__ is {__name__} :(")
import test2

WIDTH = 64
HEIGHT = 64
hub = hub75.Hub75(WIDTH, HEIGHT, stb_invert=True)
hub.start()

black = hub75.color(0, 0, 0)
white = hub75.color(255, 255, 255)

print(f"fm6166a={hub75.PANEL_FM6126A}")
print(f"generic={hub75.PANEL_GENERIC}")
print(f"black={black}")
print(f"white={white}")

hub.set_rgb(2, 2, 100, 100, 100)
hub.flip()

while True:
    c = sys.stdin.read(1)
    print(f"'{c}' - {type(c)}")

#rgb_sets = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1]]
#line = -31
#while True:
#    time.sleep(0.01)

#    for i in range(8):
#        rgb = rgb_sets[i]
#
#        for n in range(256):
#            y = int(n/64) + 4 * i + line
#            if (y >= 0 and y <= 63):
#                matrix.set_rgb(n % 64, y, rgb[0] * n, rgb[1] * n, rgb[2] * n)
#
#    line += 1
#    if line >= 62:
#        line = -31
#
#    matrix.flip()

#hub.clear()
#hub.flip()

#while True:
#    h = time.ticks_ms() / 5000.0
#    hub.set_all_hsv(h, 1.0, 1.0)
#    for y in range(8):
#        for x in range(WIDTH):
#            c = int(x * 255 / WIDTH)
#            hub.set_rgb(x, y, c, c, c)
#    for x in range(WIDTH):
#        hub.set_rgb(x, x, 255, 0, 0)
#        hub.set_rgb(WIDTH - 1 - x, x, 255, 0, 0)
#    hub.flip()
#    time.sleep(1.0 / 60)