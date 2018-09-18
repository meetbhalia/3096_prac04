#!/usr/bin/python

import spidev
import time
import os
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# pin definition
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI,
miso=SPIMISO)

# global variable
values = [0]*8

while True:
    for i in range(8):
        values[i] = mcp.read_adc(i)

# function to convert data to voltage level,
# places: number of decimal places needed
def ConvertVolts(data,places):
    volts = (data * 3.3) / float(1023)
    volts = round(volts,places)
    return volts

#function to convert data to degree celcius
def ConvertToDegrees(data,places):
    temp = (((ConvertVolts(data,places))-0.5)/0.01)
    temp = round(temp,places)
    return temp

#function to convert data to percentage light
def ConvertToLight(data,places):
    light = (((ConvertVolts(data,places))/3.3)*100)
    light = round(light,places)
    return light

# function definition: threaded callback
#def callback1(channel):
    
    
# Under a falling-edge detection, regardless of current execution
# callback function will be called
#GPIO.add_event_detect(switch_1, GPIO.FALLING, callback=callback1,
#bouncetime=200)

# Define delay between readings
delay = 2

try:
    while True:
        # Read the data
 
        # Wait before repeating loop
        time.sleep(delay)
except KeyboardInterrupt:
    spi.close()
