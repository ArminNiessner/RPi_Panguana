
 # Copyright (C) 2019  Armin Niessner
 
 # This program is free software: you can redistribute it and/or modify
 # it under the terms of the GNU General Public License as published by
 # the Free Software Foundation, either version 3 of the License, or
 # (at your option) any later version.
 
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # GNU General Public License for more details.
 
 # You should have received a copy of the GNU General Public License
 # along with this program. If not, see <https://www.gnu.org/licenses/>.


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 14:44:50 2019

@author: Armin Niessner
"""

import os
import time
from ADCDifferentialPi import ADCDifferentialPi
from sht_sensor import Sht
import threading
from datetime import datetime
import bme280
from ftplib import FTP
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
adc = ADCDifferentialPi(0x6A, 0x6B, 18)
sht = Sht(5, 6)

GPIO.setup(13, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(20, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

start_time = time.time()
interval = 60 # set interval in seconds
filepath = "/home/pi/datalog_pi.csv"

def ftp_upload():
    server = 'ftp.name.org'
    username = 'username'
    password = 'password'

    try:
        ftp_connection = FTP(server, username, password)
        fh = open("/home/pi/Desktop/datalog_pi.csv", 'rb')
        ftp_connection.storbinary('STOR datalog_pi.csv', fh)
        fh.close()
    except FileNotFoundError:
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

def log_data():
    global rain_count
    global wsp_count
    global filepath
    
    file = open(filepath, "a")
    if os.stat(filepath).st_size == 0:
        file.write("Time,TMP,RH,SRD,RAIN,WSP,WDIR,PRESS,TBMP\n")
    
    cdatetime = datetime.now()
    currentDate = cdatetime.strftime('%Y-%m-%d %H:%M:%S')
    humidity = round(sht.read_rh(),1)
    temperature = round(sht.read_t(),1)
    radiation = round(adc.read_voltage(1)  * 1000,2)
    rain = rain_count
    rain_count = 0
    windspeed = wsp_count
    wsp_count = 0
    winddir = round(adc.read_voltage(2) * 1000,2)
    temp_bmp, pressure, humidity_fake = bme280.readBME280All()
    temp_bmp = round(temp_bmp,1)
    pressure = round(pressure,1)

    file.write(currentDate + "," + str(temperature) + "," + str(humidity)
               + "," + str(radiation) + "," + str(rain) + ","
               + str(windspeed) + "," + str(winddir) + "," + str(pressure)
               + "," + str(temp_bmp) + "\n")
    
    file.flush()
    #ftp_upload()
    
log_data()
