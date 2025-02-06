import gc
import os
import machine


from WIFI_CONFIG import SSID, PSK, CONFIGURED
from sprites import draw_tick, draw_cross, draw_text, draw_rectangle, draw_ip_address
import network
import socket
import time
import hub75
import matrix_details
import machine
import utime
matrix = hub75.Hub75(matrix_details.DISPLAY_WIDTH, matrix_details.DISPLAY_HEIGHT, stb_invert=True)
matrix.start()

mdi_file = open("matrix-display-coloured.mdi", "rb")
mdi_data = mdi_file.read()
mdi_file.close()
print(f"file size = {len(mdi_data)}")

palette_size = mdi_data[0] * 256 + mdi_data[1]
print(f"palette_size = {palette_size}")
palette = []
for n in range(palette_size):
    offset = 2 + n * 3
    r = mdi_data[offset]
    g = mdi_data[offset + 1]
    b = mdi_data[offset + 2]

    palette.append((r, g, b))

pixel_offset = 2 + palette_size * 3
matrix.clear()
for y in range(64):
    for x in range(64):
        r, g, b = palette[mdi_data[pixel_offset]]
        pixel_offset += 1
        matrix.set_rgb(x, y, r, g, b)

matrix.flip()
time.sleep(5)

ssid = "Matrix-D"
password = "12345678"

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password) 
ap.active(True)

max_wait = 20
while not ap.active:
    matrix.clear()
    draw_text(2, 2, "Matrix-D:", matrix.set_rgb, 255, 255, 255)
    draw_rectangle(56, 2, max_wait, 5, matrix.set_rgb, 0, 128, 255)
    matrix.flip()
    sleep(1)

print("Access point active")
print(ap.ifconfig())
#time.sleep(5000)
#wlan = network.WLAN(network.STA_IF)
#wlan.active(True)
#wlan.connect(SSID, PSK)

#max_wait = 20
#while max_wait > 0:
#    matrix.clear()
#    draw_text(2, 2, "WIFI:", matrix.set_rgb, 255, 255, 255)
#    draw_rectangle(32, 2, max_wait, 5, matrix.set_rgb, 0, 128, 255)
#    matrix.flip()
    
#    if wlan.status() < 0 or wlan.status() >= 3:
#        break
    
#    max_wait -= 1
#    print('waiting for connection...')
#    time.sleep(1)

#if wlan.status() != 3:
#    matrix.clear()
#    draw_text(2, 2, "WIFI:", matrix.set_rgb, 255, 255, 255)
#    draw_text(32, 2, "FAIL", matrix.set_rgb, 255, 0, 0)
#    draw_sad_face(56, 2, matrix.set_rgb, 255, 0, 0)
#    matrix.flip()
#    print('network connection failed')
#    time.sleep(2)
#    machine.reset()


#print('connected')
#status = wlan.ifconfig()
#print( 'ip = ' + status[0] )

mdi_file = open("setup-screen.mdi", "rb")
mdi_data = mdi_file.read()
mdi_file.close()
print(f"file size = {len(mdi_data)}")

palette_size = mdi_data[0] * 256 + mdi_data[1]
print(f"palette_size = {palette_size}")
palette = []
for n in range(palette_size):
    offset = 2 + n * 3
    r = mdi_data[offset]
    g = mdi_data[offset + 1]
    b = mdi_data[offset + 2]

    palette.append((r, g, b))

pixel_offset = 2 + palette_size * 3
matrix.clear()
for y in range(64):
    for x in range(64):
        r, g, b = palette[mdi_data[pixel_offset]]
        pixel_offset += 1
        matrix.set_rgb(x, y, r, g, b)

matrix.flip()



while True:
    canvas_socket = socket.socket()
    canvas_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    canvas_socket.bind(("0.0.0.0", 80))
    canvas_socket.listen(1)
    #connection, _ = canvas_socket.accept()
    #connection_open = True
    html=webpage()
    print("running web server")
    
    while True:
        client, _ = canvas_socket.accept()
        print(f"connected: {client}")
        data = client.recv(800)
        print(f"Receieved {data}")
        print(data)
        client.send(html)
        client.close()
        
    try:
        while connection_open:
            x = 0
            y = 0
            rgb_index = 0

            while y < 64:
                data = connection.recv(800)
                if len(data) == 0:
                    connection_open = False
                    break

                for value in data:
                    if rgb_index == 0:
                        r = value
                        rgb_index = 1
                    elif rgb_index == 1:
                        g = value
                        rgb_index = 2
                    else:
                        b = value
                        rgb_index = 0
                        
                        matrix.set_rgb(x, y, r, g, b)
                        x += 1
                        if x >= 64:
                            x = 0
                            y += 1

            matrix.flip()
            print("redraw")
            connection.send("0")

        raise OSError("")
    
    except OSError as _:
        canvas_socket.close()
        matrix.clear()
        matrix.flip()
        print("Lost connection. Starting again")


