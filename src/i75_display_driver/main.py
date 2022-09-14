import sys

# If the platform is rp2, then this is running on the interstate 75, otherwise
# it's running on a RPI/PC. If the former. add the project's library paths to 
# the list searched when import is used before importing packages and modules
if sys.platform == 'rp2':
    sys.path.append('/brokers') 
    sys.path.append('/graphics')

import hub75 # type: ignore

WIDTH = 64
HEIGHT = 64
matrix = hub75.Hub75(WIDTH, HEIGHT, stb_invert=True)
matrix.start()


