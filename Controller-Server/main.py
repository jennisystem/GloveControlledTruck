# SERVER  / CONTROLLER

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
#
# WSGI_simpletest modified for the Feather M4, Airlift, and EE11SC

import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import neopixel

from adafruit_esp32spi import adafruit_esp32spi
import adafruit_esp32spi.adafruit_esp32spi_wifimanager as wifimanager
import adafruit_esp32spi.adafruit_esp32spi_wsgiserver as server
from adafruit_wsgi.wsgi_app import WSGIApp

import time

t = 0.15   # default time


###--------------- NEOPIXEL ----------------###
# set up the neopixel for the Feather M4
num_color = 0
pixel_pin = board.NEOPIXEL

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
ORDER = neopixel.GRBW

pixel = neopixel.NeoPixel(
    pixel_pin, 1, brightness=0.2, auto_write=False, pixel_order=ORDER)
###-------------------------------------------###


###--------------- WIFI SETUP ----------------###
# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

print("ESP32 SPI simple web app test!")

# NOTE: You may need to change the pins to reflect your wiring
esp32_cs = DigitalInOut(board.D10)
esp32_ready = DigitalInOut(board.D9)
esp32_reset = DigitalInOut(board.D6)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(
    spi, esp32_cs, esp32_ready, esp32_reset)

## To you want to create an un-protected WIFI hotspot to connect to with secrets:"
secrets = {"ssid": "yeehaw"}
wifi = wifimanager.ESPSPI_WiFiManager(esp, secrets)
wifi.create_ap()

# Here we create our application, registering the
# following functions to be called on specific HTTP GET requests routes

web_app = WSGIApp()

###-------------------- DEFAULT MOVEMENTS ---------------------###
movement = "NONE"
clear = False
changed = False
flex = False

'''
## If you want to connect to wifi with secrets:
wifi = wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light, debug=True)
wifi.connect()

## If you want to create a WIFI hotspot to connect to with secrets:
# secrets = {"ssid": "My ESP32 AP!", "password": "supersecret"}
# wifi = wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)
# wifi.create_ap()
'''


###------------------------- MOVE FUNCTIONS --------------------###
def send_right():
    print("R")


def send_left():
    print("L")

def send_forward(t):
    print("F")
    with DigitalInOut(board.D11) as forward:
        forward.direction = Direction.OUTPUT
        forward.value = False
        time.sleep(t)


def send_backward(t):
    print("B")
    with DigitalInOut(board.D12) as backward:
        backward.direction = Direction.OUTPUT
        backward.value = True
        time.sleep(t)


def send_command(command):
    global t
    if command == "forward":
        send_forward(t)
    elif command == "backward":
        send_backward(t)
    elif command == "right":
        send_right(t)
    elif command == "left":
        send_left(t)


###----------------------------WEBPAGES-----------------------###
@web_app.route("/isflexed")
def is_flexed(request):
    global flex
    if flex:
        return ("200 OK", [], f"{flex}")
    else:
        return ("400 Error", [], f"{flex}")

@web_app.route("/flex/<bit>")
def flex_data(request, bit):
    bit = int(bit)
    global flex
    if bit == 0:
        flex = False
        print(f"Flex: {flex}")
        return ("200 OK", [], "No flex")
    else:
        flex = True
        print(f"Flex: {flex}")
        return ("200 OK", [], "Flexed!")

@web_app.route("/clear/<bit>")
def route_clear(request, bit):
    global clear
    bit = int(bit)
    print(bit)
    if bit == 0:
        clear = False
        return ("200 OK", [], "NOT ALLOWED")
    else:
        clear = True
        return ("200 OK", [], "ALLOWED")

@web_app.route("/control/<bit>")
def print_control(request, bit):
    global num_color
    global changed
    global movement

    changed = True
    bit = int(bit)
    num_color = bit
    if bit == 0:
        movement = "stop"
        return ("200 OK", [], movement)
    elif bit == 1:
        movement = "forward"
        return ("200 OK", [], movement)
    elif bit == 2:
        movement = "backward"
        return ("200 OK", [], movement)
    elif bit == 3:
        movement = "left"
        return ("200 OK", [], movement)
    elif bit == 4:
        movement = "right"
        return ("200 OK", [], movement)
    else:
        movement = "NONE"
        return ("200 OK", [], movement)

'''def show_color(num):
    if num == 0:
        pixel.fill((0, 0, 0))
        pixel.show()
    elif num == 1:
        pixel.fill((255, 0, 0))
        pixel.show()
    elif num == 2:
        pixel.fill((0, 255, 0))
        pixel.show()
    elif num == 3:
        pixel.fill((0, 0, 255))
        pixel.show()
    elif num == 4:
        pixel.fill((255, 255, 255))
        pixel.show()'''



# Here we setup our server, passing in our web_app as the application
server.set_interface(esp)
wsgiServer = server.WSGIServer(80, application=web_app)

print("open this IP in your browser: ", esp.pretty_ip(esp.ip_address))

# Start the server
wsgiServer.start()
while True:
    # Our main loop where we have the server poll for incoming requests
    try:
        changed = False
        wsgiServer.update_poll()
        # Could do any other background tasks here, like reading sensors
        if changed and clear:
            send_command(movement)
            print(movement)
            #show_color(num_color)
    except (ValueError, RuntimeError) as e:
        print("Failed to update server, restarting ESP32\n", e)
        wifi.reset()
        continue





