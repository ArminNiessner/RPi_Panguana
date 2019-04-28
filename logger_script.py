#!/usr/bin/env python3
"""
 Copyright (C) 2019  Armin Niessner
 
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program. If not, see <https://www.gnu.org/licenses/>.


Created on Fri Mar  1 14:44:50 2019

@author: armin

"""

# logs every "interval" seconds and appends values to file
# on every log new values are appended to a file at taysira.org/aniessner/
# if upload fails, file to append is incrementing, if upload is successful, file to append is cleared
# every month a new file is created
# the whole file is uploaded at programm start

import os
import time
from ADCDifferentialPi import ADCDifferentialPi
from sht_sensor import Sht
import threading
from datetime import datetime
from random import randint
from random import uniform
import bme280
from ftplib import FTP
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
adc = ADCDifferentialPi(0x6A, 0x6B, 18)
sht = Sht(5, 6)

GPIO.setup(13, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(20, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(17, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(27, GPIO.OUT, initial = GPIO.HIGH)

start_time = time.time()
interval = 60 # set interval in seconds
#interval_up = 60 # upload after x logs, 1440 for once a day
path = "/home/pi/"
#n_log = 0

server = 'ftp.name.org'
username = 'username'
password = 'password'

def ftp_upload(filepath, filename):    
    try:
        ftp_connection = FTP(server, username, password)
        fh = open(filepath, 'rb')
        ftp_connection.storbinary('APPE ' + filename, fh, 1)
        fh.close()
        fh2 = open(filepath, "w")
        fh2.seek(0)
        fh2.truncate()
        fh2.close()
    except:
        print("fail1")
        pass

def ftp_upload_all(filepath, filename):
    try: 
        ftp_connection = FTP(server, username, password)
        fh = open(filepath, "rb")
        ftp_connection.storbinary("STOR " + filename, fh)
    except:
        print("fail")
        pass

rain_count = 0
wsp_count = 0

def rain_callback(channel):
    global rain_count
    rain_count += 1

def wsp_callback(channel):
    global wsp_count
    wsp_count += 1
    
GPIO.add_event_detect(18, GPIO.FALLING, callback=rain_callback, bouncetime=200)
GPIO.add_event_detect(19, GPIO.FALLING, callback=wsp_callback, bouncetime=200)

year_s = str(datetime.now().year)
month_is = datetime.now().month
if month_is < 10:
    month_s = "0" + str(month_is)
else:
    month_s = str(month_is)
filename_s = "pang_pi_{}{}.csv".format(year_s, month_s)
filepath_s = "{}{}".format(path, filename_s)
file_s = open(filepath_s, "a")
ftp_upload_all(filepath_s, filename_s)
file_s.flush()
file_s.close()

def log_data():
    global rain_count
    global wsp_count
    global path
    global interval
   # global n_log
    year = str(datetime.now().year)
    month_i = datetime.now().month
    minute = datetime.now().minute
    if month_i < 10:
        month = "0" + str(month_i)
    else:
        month = str(month_i)
    filename = "pang_pi_{}{}.csv".format(year, month)
    fn_append = "pang_append.csv"
    filepath = "{}{}".format(path, filename)
    fp_append = "{}{}".format(path, fn_append)
    threading.Timer(interval, log_data).start()
    file = open(filepath, "a")
    if os.stat(filepath).st_size == 0:
        file.write("Time,TMP,RH,DEW,SRD,RAIN,WSP,WDIR,PRESS,TBMP,TMPO,RHO\n")
    
    cdatetime = datetime.now()
    currentDate = cdatetime.strftime('%Y-%m-%d %H:%M:%S')
    try:
        humidity = round(sht.read_rh(),1)
        if humidity > 100:
            humidity = 100
        temperature = round(sht.read_t(),1)
        dew = round((humidity/100)**(1/8) * (112 + 0.9 * temperature) + 0.1 * temperature - 112,1)

    except:
        humidity = "NaN"
        temperature = "NaN"
        dew = "Nan"
    radiation = adc.read_voltage(1) * 1000 - 8
    if radiation < 0:
        radiation = 0
    radiation = round(radiation, 1)
    rain = round(rain_count * 0.2175641068, 2)
    rain_count = 0
    windspeed = round((wsp_count*1.25)/60, 2)
    wsp_count = 0
    Vref = adc.read_voltage(2)
    winddir = int(adc.read_voltage(3) / Vref * 360)
    temp_o = round(adc.read_voltage(5)*100 - 30, 1)
    rh_o = round(adc.read_voltage(6)*100, 1)
    try:
        temp_bmp, pressure, humidity_fake = bme280.readBME280All()
        temp_bmp = round(temp_bmp,1)
        pressure = round(pressure,1)
    except:
        temp_bmp = "NaN"
        pressure = "NaN"

    file_append = open(fp_append, "a")

    file.write(currentDate + "," + str(temperature) + "," + str(humidity) +  "," + str(dew)
               + "," + str(radiation) + "," + str(rain) + ","
               + str(windspeed) + "," + str(winddir) + "," + str(pressure)
               + "," + str(temp_bmp) + "," + str(temp_o) + "," + str(rh_o) + "\n")

    file_append.write(currentDate + "," + str(temperature) + "," + str(humidity) + "," + str(dew)
               + "," + str(radiation) + "," + str(rain) + ","
               + str(windspeed) + "," + str(winddir) + "," + str(pressure)
               + "," + str(temp_bmp) + "," + str(temp_o) + "," + str(rh_o) + "\n")
    ftp_upload(fp_append, filename)
       # n_log = 0
    file.flush()
    file.close()
    file_append.flush()
    file_append.close()
   # n_log += 1
    
log_data()
