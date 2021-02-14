#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import *
import argparse
import datetime

# LED strip configuration:
LED_COUNT      = 110      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

LAST_MINUTE_ENTRY = 0

AS_ISCH = [109, 108, 106, 105, 104, 103]
M_FUF = [101, 100, 99]
M_ZAA = [96, 97, 98]
M_VIERTU = [88, 89, 90, 91, 92, 93]
M_ZWANZG = [87, 86, 85, 84, 83, 82]
VOR = [79, 78, 77]
AB = [66, 67]
M_HAUBI = [69, 70, 71, 72, 73]
EUFI = [15, 14, 13, 12]
FUFI = [50, 51, 52, 53]
EIS = [65, 64, 63]
ZWOI = [62, 61, 60, 59]
DRU = [57, 56, 55]
VIERI = [44, 45, 46, 47, 48]
SACHSI = [43, 42, 41, 40, 39, 38]
ACHTI = [22, 23, 24, 25, 26]
SIBNI = [37, 36, 35, 34, 33]
ZWOUFI = [3, 4, 5, 6, 7, 8]
ZANI = [21, 20, 19, 18]
NUNI = [28, 29, 30, 31]

# rosa 250,9,251
# blauviolette 25,9,251
# dunkelviolette 119,62,255

def drawMatrix(strip):
  time_has_changed(True)
  array = create_time_array(strip)
  display_array(strip, Color(255,255,255), array)

  while True:
    if time_has_changed(False) == True:
      array = create_time_array(strip)
      display_array(strip, Color(255,255,255), array)
    else:
      time.sleep(10)

def display_array(strip, color, array):
  for i in range(strip.numPixels()):
    if array.__contains__(i):
      strip.setPixelColor(i, color)
    else:
      strip.setPixelColor(i, Color(0,0,0))
  strip.show()

def create_time_array(strip):
  now = datetime.datetime.now()
  hour = now.hour
  time_array = []
  last_min = LAST_MINUTE_ENTRY
  if hour == 7 and last_min == 00 or hour == 15 and last_min == 10:
    rainbow(strip)
  if last_min == 55:
    theaterChase(strip, Color(127,127,127), 50, 30)
  time_array = time_array + AS_ISCH + minutes()
  # print("hour: ", hour)
  if last_min <= 20:
    time_array = time_array + hours(hour)
  else:
    time_array = time_array + hours(hour + 1)
  # print("Time array: ", time_array)
  return time_array

def minutes():
  minute = LAST_MINUTE_ENTRY
  if minute == 5:
    return M_FUF + AB
  elif minute == 10:
    return M_ZAA + AB
  elif minute == 15:
    return M_VIERTU + AB
  elif minute == 20:
    return M_ZWANZG + AB
  elif minute == 25:
    return M_FUF + VOR + M_HAUBI
  elif minute == 30:
    return M_HAUBI
  elif minute == 35:
    return M_FUF + AB + M_HAUBI
  elif minute == 40:
    return M_ZWANZG + VOR
  elif minute == 45:
    return M_VIERTU + VOR
  elif minute == 50:
    return M_ZAA + VOR
  elif minute == 55:
    return M_FUF + VOR
  else:
    return []

def hours(next_hour):
  if next_hour == 1 or next_hour == 13:
    return EIS
  if next_hour == 2 or next_hour == 14:
    return ZWOI
  if next_hour == 3 or next_hour == 15:
    return DRU
  if next_hour == 4 or next_hour == 16:
    return VIERI
  if next_hour == 5 or next_hour == 17:
    return FUFI
  if next_hour == 6 or next_hour == 18:
    return SACHSI
  if next_hour == 7 or next_hour == 19:
    return SIBNI
  if next_hour == 8 or next_hour == 20:
    return ACHTI
  if next_hour == 9 or next_hour == 21:
    return NUNI
  if next_hour == 10 or next_hour == 22:
    return ZANI
  if next_hour == 11 or next_hour == 23:
    return EUFI
  if next_hour == 12 or next_hour == 00 or next_hour == 24:
    return ZWOUFI

def rainbow(strip, wait_ms=20, iterations=1):
  """Draw rainbow that fades across all pixels at once."""
  for j in range(2*iterations):
    for i in range(strip.numPixels()):
      strip.setPixelColor(i, wheel((i*j) & 255))
      strip.show()
      time.sleep(wait_ms/1000.0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

# Returns true every time a new 5 minutes have started on the clock
# i.E it's now 00:35 or 00:10
def time_has_changed(isStartup):
    global LAST_MINUTE_ENTRY
    now = datetime.datetime.now()
    if isStartup == True:
        LAST_MINUTE_ENTRY = round(now.minute / 5) * 5 #round to nearest five
        return True
    if LAST_MINUTE_ENTRY != now.minute:
        if now.minute % 5 == 0:
            LAST_MINUTE_ENTRY = now.minute
            return True
    return False

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(5/100)
        strip.setPixelColor(i, Color(0,0,0))
        strip.show()

def wipeStrip(strip, color, wait_ms=5):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000)

# Main program logic follows:
if __name__ == '__main__':
  # Process arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
  args = parser.parse_args()

  # Create NeoPixel object with appropriate configuration.
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
  # Intialize the library (must be called once before other functions).
  strip.begin()

  print ('Press Ctrl-C to quit.')
  if not args.clear:
    print('Use "-c" argument to clear LEDs on exit')

  try:
    drawMatrix(strip)
  except KeyboardInterrupt:
    if args.clear:
      wipeStrip(strip, Color(0,0,0), 10)
