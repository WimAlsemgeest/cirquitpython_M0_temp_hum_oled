# ----------------------------------------------------------------------------
#   Demo program using CircuitPython
#
#   Used:
#       Adafruit Metro express M0 controller
#       Adafruit si7021 sensor
#       Adafruit ssd1306 oled display 128x64 monochrome
#
#   by:
#       Wim Alsemgeest, used parts of Adafruits examples.
# ----------------------------------------------------------------------------
import time
import adafruit_si7021
import adafruit_ssd1306
import board
import busio
from digitalio import DigitalInOut

# ----------------------------------------------------------------------------
#   Scan the I2C bus for devices and print them once.
# ----------------------------------------------------------------------------
i2c = busio.I2C(board.SCL, board.SDA)
# Lock the I2C device before we try to scan
while not i2c.try_lock():
    pass
# Print the addresses found once
print("I2C addresses found:", [hex(device_address)
                               for device_address in i2c.scan()])

# Unlock I2C now that we're don scanning.
i2c.unlock()

# ----------------------------------------------------------------------------
#   Create for used devices on our I2C port.
# ----------------------------------------------------------------------------
si7021 = adafruit_si7021.SI7021(i2c)    # Sensor temperature, humidity
reset_pin = DigitalInOut(board.D4)      # Reset pin for oled display
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3d, reset=reset_pin)

# ----------------------------------------------------------------------------
#   Setting up some variables
# ----------------------------------------------------------------------------
HEADTEXT = 'Pyton Cave'
FOOTERTEXT = 'Loc: Naaldwijk'

# ----------------------------------------------------------------------------
#   Draw the head of the oled page.
# ----------------------------------------------------------------------------


def draw_head(text, pos):
    """Draw a outline with a text in it on top of display"""
    for pix in range(0, 128, 1):
        oled.pixel(pix, 0, 1)
        oled.pixel(pix, 14, 1)
    for piy in range(0, 14, 1):
        oled.pixel(0, piy, 1)
        oled.pixel(127, piy, 1)
    oled.text(text, pos, 3)
# ----------------------------------------------------------------------------
#   Draw the footer of the oled page.
# ----------------------------------------------------------------------------


def draw_footer(text, pos):
    """Draw a outline with a text in it on bottom of display"""
    for pix in range(0, 128, 1):
        oled.pixel(pix, 52, 1)
        oled.pixel(pix, 63, 1)
    for piy in range(52, 63, 1):
        oled.pixel(0, piy, 1)
        oled.pixel(127, piy, 1)
    oled.text(text, pos, 54)

# ----------------------------------------------------------------------------
#   Clear an area of the screen because pixels overwrite eachother
# ----------------------------------------------------------------------------


def clear_data_area(start, end):
    """Clear the section of diplay where data is printend."""
    for i in range(start, end, 1):
        for j in range(0, 128, 1):
            oled.pixel(j, i, 0)


# ----------------------------------------------------------------------------
#   Start of program.
# ----------------------------------------------------------------------------
oled.fill(0)
draw_head(HEADTEXT, 20)
draw_footer(FOOTERTEXT, 5)

while True:
    # ------------------------------------------------------------
    #   Create strings from the measurements
    # ------------------------------------------------------------
    temp_string = '{:.1f} degrees C'.format(si7021.temperature)
    hum_string = 'Humidity {:.1f} %'.format(si7021.relative_humidity)

    # print(temp_string)            # Debuging to terminal
    # print(hum_string)             # Debuging to terminal
    clear_data_area(20, 50)         # Clear space for putting results
    oled.text(temp_string, 5, 20)   # Put temperature
    oled.text(hum_string, 2, 35)    # Put humidity
    oled.show()                     # Show it all
    time.sleep(5)
