#
# This is the default implementation of this module. For devices that don't use r >> 16, g >> 8, b >> 0
# packing of rgb into an int (like neo pixels, which use grb), alternative packing bit shits can be handled by pushing
# custom versions of this module to the target RPI/Pico.
#

RED_BIT_SHIFT: int = 16
GREEN_BIT_SHIFT: int = 8
BLUE_BIT_SHIFT: int = 0
