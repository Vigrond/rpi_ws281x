#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse
import numpy as np
from datetime import datetime

# LED strip configuration:
#LED_COUNT      = 1016      # Number of LED pixels.
LED_COUNT      = 72*4 + 57
#LED_COUNT = 60
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255    # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

timer_on = False

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

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

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def morph(from_color, to_color, percent):
    color1 = np.array(from_color)
    color2 = np.array(to_color)
    vector = color2 - color1
    new_color = color1 + vector * (percent/100.0)
    return new_color.astype(int)

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

group1 = []
group2 = []
red = (175,0,0)
green = (0,255,0)
blue = (0,0,255)
purp = (0,50,255)
grey = (95,95,95)
orange = (75, 255, 0)

#red = green
#green = grey
num_pixels = strip.numPixels()

group = 5
for pixel in range(0, num_pixels):
    if pixel%(group*2) == 0:
        first = (pixel for pixel in range(pixel, pixel+group))
        second = (pixel for pixel in range(pixel+group, pixel+group*2))
        for pixel in first:
            if pixel <= num_pixels:
                group1.append(pixel)
        for pixel in second:
            if pixel <= num_pixels:
                group2.append(pixel)

def xmas_alternate(strip, wait_ms=100, iterations=2):
    for j in range(iterations):
        step = j == 0
        from_color = red if step else green
        to_color = green if step else red

        for fade in range(1, 100, 10):
            for pixel in group1:
                strip.setPixelColor(pixel, Color(*morph(from_color, to_color, fade)))
            for pixel in group2:
                strip.setPixelColor(pixel, Color(*morph(to_color, from_color, fade)))

            strip.show()
            time.sleep(wait_ms/1000.0)

def xmas_snake(strip, wait_ms=50, iterations=9):
    snake_red = list(group1)
    snake_green = list(group2)

    for pixel in snake_red:
        strip.setPixelColor(pixel, Color(*red))
    for pixel in snake_green:
        strip.setPixelColor(pixel, Color(*green))
    strip.show()
    time.sleep(wait_ms/1000.0)

    for round in range(iterations):
        for index, pixel in enumerate(snake_red):
            if index % 5 == 4:
                strip.setPixelColor(pixel+1, Color(*red))
                snake_red[index] += 1
            elif index % 5 == 0:
                strip.setPixelColor(pixel, Color(*green))
                snake_red[index] += 1
        if round >= 5:
            strip.setPixelColor(round-5, Color(*red))

        strip.show()
        time.sleep(wait_ms/1000.0)

def full_white(strip, wait_ms=50, iterations=100):
    for iteration in range(iterations):
        modifier = iteration/float(iterations);
        value = int(modifier*255)
        white = Color(value, value, value)
        for pixel in range(num_pixels):
            strip.setPixelColor(pixel, white)
        strip.show()
        time.sleep(wait_ms/1000.0)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()



    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            now = datetime.now()
            if timer_on and now.hour >= 2 and now.hour < 18:
                print ('hour is {}. off schedule.'.format(now.hour))
                for pixel in range(num_pixels):
                    strip.setPixelColor(pixel, 0)
                strip.show()
                time.sleep(10)
                continue
            #print ('Color wipe animations.')
            #colorWipe(strip, Color(255, 0, 0))  # Red wipe
            #colorWipe(strip, Color(0, 255, 0))  # Blue wipe
            #colorWipe(strip, Color(0, 0, 255))  # Green wipe
            #print ('Theater chase animations.')
            #theaterChase(strip, Color(127, 127, 127))  # White theater chase
            #theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            #theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            #print ('Rainbow animations.')
            #rainbow(strip)
            #rainbowCycle(strip)
            #theaterChaseRainbow(strip)
            #xmas_snake(strip)
            #xmas_alternate(strip)
            full_white(strip)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
