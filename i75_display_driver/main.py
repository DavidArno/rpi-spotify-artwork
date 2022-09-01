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

for n in range(256):
    matrix.set_rgb(int(n/64), n % 64, n, 0, 0)

matrix.flip()