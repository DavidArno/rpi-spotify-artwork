import serial
import base64
import time
import sys

print(serial.VERSION)
 
ser = serial.Serial('/dev/ttyACM0',
             baudrate=115200,
             timeout=None,
             stopbits = serial.STOPBITS_ONE,
             bytesize = serial.EIGHTBITS,
             rtscts = False,
             dsrdtr = False)

print("Opened.")

while True:
    line = sys.stdin.readline()
    if line[0] == 'x':
        ser.close()
        quit()
    else:
        if line[0] != '?':
            for c in [x for x in line if x != '\r' and x != '\n']:
                print(f"Sending: {c}")
                ser.write(c.encode())
        time.sleep(0.5)
        while ser.in_waiting > 0: 
            response = ser.readline()
            print(f"Response: {response}")
            time.sleep(0.5)

