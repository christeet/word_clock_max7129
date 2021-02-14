import time
import board
import busio
from rpi_ws281x import *

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# LED strip configuration:
LED_COUNT      = 11      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 0     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1015(i2c)
ads.gain = 1

chan = AnalogIn(ads, ADS.P2)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

strip.begin()

while True:
  print("ChanVal: ", chan.value)
  print("ChanVolt: ", chan.voltage)
  brightness = int(round(255/9000*chan.value))
  print("Brightness: ", brightness)
  for i in range(strip.numPixels()):
    strip.setPixelColor(i, Color(255, 255, 255))
  strip.setBrightness(brightness)
  strip.show()
  time.sleep(2)
