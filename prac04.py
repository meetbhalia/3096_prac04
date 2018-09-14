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

# Open SPI bus
spi = spidev.SpiDev() # create spi object
spi.open(0,0)

# function to read ADC data from a channel
def GetData(channel): # channel must be an integer 0-7
    adc = spi.xfer2([1,(8+channel)<<4,0]) # sending 3 bytes
    data = ((adc[1]&3) << 8) + adc[2]
    return data

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

# Define sensor channels
temp_data = GetData (0)
light_data = GetData (7)

# Define delay between readings
delay = 2

try:
    while True:
        # Read the data
        #sensor_temp = ConvertToDegrees(temp_data,2)
        #sensor_light = ConvertToLight(light_data,2)
        #print (sensor_temp)
        print ((temp_data))
        #print (sensor_light)
        print ((light_data))
        # Wait before repeating loop
        time.sleep(delay)
except KeyboardInterrupt:
    spi.close()