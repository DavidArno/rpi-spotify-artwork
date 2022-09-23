################################################################################
# To use these shims in micropython:
# 1. Create a directory, /shims, on the microcontroller
# 2. Copy this file, shim_setup.py to / or /lib on the microcontroller
# 3. In eg main.py, import shim_setup.py
# If running on micropython, this then adds shims to the sys path. If on
# cpython, it does nothing and the standard libraries are used instead.
################################################################################ 
try:
    import micropython # type: ignore
    import sys
    sys.path.append('/shims')
except: pass