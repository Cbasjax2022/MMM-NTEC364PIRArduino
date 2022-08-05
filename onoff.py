#!/usr/bin/python

from _thread import start_new_thread
import serial
import pigpio
import tty
import termios
import sys
import time
import os
import subprocess
from datetime import datetime
import gspread

# DEFINE VARIABLES
# SECRET CREDENTIALS FILE
gc = gspread.service_account(filename='apicredentials.json')
# API KEY
sh = gc.open_by_key('1DorK1dQWwjlAj4ZiZ9OE_o8lVTSwrah3tS0H1yJ9ctc')

worksheet = sh.sheet1
now = datetime.now()

# Function to find next empty row in spreadsheet


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)


RED_PIN = 17
GREEN_PIN = 22
BLUE_PIN = 24


bright = 255
r = 255.0
g = 0.0
b = 0.0

pi = pigpio.pi()


def setLights(pin, brightness):
    realBrightness = int(int(brightness) * (float(bright) / 255.0))
    pi.set_PWM_dutycycle(pin, realBrightness)


tmp = os.popen("sudo /opt/vc/bin/tvservice -s").read()
if tmp.find("off") == -1:
    print("monitor is on")
    next_row = next_available_row(worksheet)
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

    # update_acell uses "a1, b7,etc cell notation.
    # update_cell uses "1, 1" cell notation as in 1st row 1st column.
    # The following line updates the A column and uses string substitution to \
    # dynamically assign the next available row in the sheet
    worksheet.update_acell("A{}".format(next_row), current_datetime)
    # diagnostic output
    print("wrote {} row to spreadsheet".format(i+1))


else:
    print("monitor is off")
    os.system("tvservice -p")
    setLights(RED_PIN, sys.argv[1])
    setLights(GREEN_PIN, sys.argv[1])
    setLights(BLUE_PIN, sys.argv[1])

    try:
        ser = serial.Serial('/dev/ttyACM0', 9600)
        time.sleep(2)
        ser.write('1')  # tell arduino to to check for gestures
        print("arduino detected")

    except serial.SerialException as e:
        # There is no new data from serial port
        print("noserial")
        pass

    time.sleep(float(sys.argv[2]))  # seconds
    os.system("tvservice -o")
    setLights(RED_PIN, 0)
    setLights(GREEN_PIN, 0)
    setLights(BLUE_PIN, 0)
    try:
        time.sleep(2)
        ser.write('0')
        ser.close()
    except serial.SerialException as e:
        # There is no new data from serial port
        # print e
        pass

pi.stop()
