#!/usr/bin/python

#import spidev
import Adafruit_MCP3008
import time
import os
#import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# pin definition
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
RESET_BUT = 17
FREQ_BUT = 27
STOP_BUT = 22
DISP_BUT = 23

GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
GPIO.setup(RESET_BUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(FREQ_BUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(STOP_BUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DISP_BUT, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

#delay to start with
delay = 0.5

#set start time
start_time = time.time()

#global variable
values = [0]*8

#global variable
recording = True

#global variable for storing
disp_num = 0

#global variable
disp_values = [[0]*5 for i in range(5)]

# Open SPI bus
#spi = spidev.SpiDev() # create spi object
#spi.open(0,0)

# function to read ADC data from a channel
#def GetData(channel): # channel must be an integer 0-7
#    adc = spi.xfer2([1,(8+channel)<<4,0]) # sending 3 bytes
#    data = ((adc[1]&3) << 8) + adc[2]
#    return data

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
#Reset button
def callback1(channel):
	#print("First callback - Reset Button on channel")
	#print(channel)
	global start_time
	start_time = time.time()
	throwaway_var = os.system('clear')

#Frequency button
def callback2(channel):
	#print("Callback 2 - Frequency Button on channel")
	#print(channel)
	global delay
	if delay==2:
		delay = 0.5
	else:
		delay = delay*2

#Stop button
def callback3(channel):
	#print("Callback 3 - Stop Button on channel")
	#print(channel)
	global recording
	global disp_num
	if recording:
		recording = False
	else:
		recording = True
		disp_num = 0

#Display button
def callback4(channel):
	#print("Callback 4 - Display Button on channel")
	#print(channel)

	print("Time		Timer		Pot	Temp	Light")
	for i in range(5):
		print("%s	%s	%4.2f V	%2d C	%2d%%"% (disp_values[i][0], disp_values[i][1],disp_values[i][2], disp_values[i][3], disp_values[i][4]))


# Under a falling-edge detection, regardless of current execution
# callback function will be called
GPIO.add_event_detect(RESET_BUT, GPIO.FALLING, callback=callback1,
bouncetime=200)

GPIO.add_event_detect(FREQ_BUT, GPIO.FALLING, callback=callback2,
bouncetime=200)

GPIO.add_event_detect(STOP_BUT, GPIO.FALLING, callback=callback3,
bouncetime=200)

GPIO.add_event_detect(DISP_BUT, GPIO.FALLING, callback=callback4,
bouncetime=200)

# Define sensor channels
#temp_data = GetData (0)
#light_data = GetData (7)


mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO)

try:
    print("Time		Timer		Pot	Temp	Light")
    while True:

	#spidev implementation
        # Read the data
        #sensor_temp = ConvertToDegrees(temp_data,2)
        #sensor_light = ConvertToLight(light_data,2)
        #print (sensor_temp)
        #print ((temp_data))
        #print (sensor_light)
        #print ((light_data))
        # Wait before repeating loop
        #time.sleep(delay)

	#Adafruit
	for i in range(8):
		values[i] = mcp.read_adc(i)

	#print values

	#Pot voltage
	Pot_volts = ConvertVolts(values[7], 4)
	#print("Pot")
	#print(Pot_volts)

	#Temp of room
	Temp_room = ConvertToDegrees(values[0], 4)
	#print("Temp")
	#print(Temp_room)

	#Light
	light_level = ConvertToLight(values[6], 4)
	#print("Light")
	#print(light_level)

	if recording:
		current_time =  time.time()
		curr_time_str = time.strftime("%X", time.localtime(current_time))
		curr_time_delta = time.strftime("%X", time.localtime(current_time-start_time))

		if disp_num<5:

			disp_values[disp_num][0] = curr_time_str
			disp_values[disp_num][1] = curr_time_delta
			disp_values[disp_num][2] = Pot_volts
			disp_values[disp_num][3] = Temp_room
			disp_values[disp_num][4] = light_level

		if disp_num<10:
			disp_num = disp_num+1

		print("%s	%s	%4.2f V	%2d C	%2d%%"% (curr_time_str,curr_time_delta, Pot_volts, Temp_room, light_level))

	#delay
	time.sleep(delay)

except KeyboardInterrupt:
#    spi.close()
     GPIO.cleanup()

GPIO.cleanup()
