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

gc = gspread.service_account(filename='MMM PIR data')
sh = gc.open_by_key('1DorK1dQWwjlAj4ZiZ9OE_o8lVTSwrah3tS0H1yJ9ctc')
worksheet = sh.sheet1
res = worksheet.get_all_records()
print(res)

now = datetime.now()

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
    # this should print out the current time
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    # writes current_date time to google sheet
    worksheet.update_cell(current_datetime)


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
