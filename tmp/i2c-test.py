import time
import board
from adafruit_bus_device.i2c_device import I2CDevice
i2c = board.I2C()
device = I2CDevice(i2c, 0x41)
count = device.write(bytes([10, 20, 80, 120, 255]))
print(count)
