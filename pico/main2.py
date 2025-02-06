### main.py
import utime
import time
from machine import mem32,Pin
import led
from i2cSlave import i2c_slave

### --- check pico power on --- ###
print("led")
led.led_power_on()

print("i2c")
### --- pico connect i2c as slave --- ###
s_i2c = i2c_slave(0,sda=20,scl=21,slaveAddress=0x41)

try:
    while True:
        data = s_i2c.get()
        print(data)

        data_int = int(data)
        for i in range(data_int):
            led.led_on()
            time.sleep(0.5)
            led.led_off()
            time.sleep(0.5)


except KeyboardInterrupt:
    pass