# RPi_Panguana
Wifi Weather Station based on a Raspberry Pi Zero W

A wifi weather station installed at the Biological Research Station Panguana, Peru. Live data can be viewed and downloaded at https://panguana-station.herokuapp.com/

## Parts

* [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)

* [ADC Differential Pi](https://www.abelectronics.co.uk/p/65/adc-differential-pi-raspberry-pi-analogue-to-digital-converter)

* [Prototype-Board](https://www.pollin.de/p/joy-it-prototyp-board-fuer-raspberry-pi-810818)

* A custom expansion board is planned combining the ADC and access to GPIOs via screw terminals

## Files

* bme280.py

* logger_script.py

* ftp_upload.py (optional)

## Libraries

* [os](https://docs.python.org/2/library/os.html)

* [time](https://docs.python.org/2/library/time.html)

* [threading](https://docs.python.org/2/library/threading.html)

* [datetime](https://docs.python.org/2/library/datetime.html)

* bme280 (available in this repository and modified from [bme280](https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/bme280.py), see also this [tutorial](https://www.raspberrypi-spy.co.uk/2016/07/using-bme280-i2c-temperature-pressure-sensor-in-python/)

* [ftplip](https://docs.python.org/2/library/ftplib.html#module-ftplib)

* [Rpi.GPIO](https://pypi.org/project/RPi.GPIO/)

* [ADCDifferentialPi](https://www.abelectronics.co.uk/kb/article/23/python-library-and-demos)

* [sht_sensor](https://pypi.org/project/sht-sensor/)

## Raspbian setup

* Download and install [ADCDifferentialPi library](https://github.com/abelectronicsuk/ABElectronics_Python_Libraries)

```
git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```

```
sudo python3 setup.py install
```

or:

```
> sudo python3.5 -m pip3 install git+https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```

* Download and install [sht_sensor library](https://github.com/kizniche/sht-sensor/)

```
pip3 install sht-sensor
```

* Download and move bme280.py to the folder where pang_logger.py is located


* execute python logging script at boot:

```
sudo nano /etc/rc.local
```

add the line: 

```
sudo python3 /home/pi/logger_script.py
```

* reconnect to wifi every hour (just in case if the wifi network is down from time to time)

```
sudo nano /usr/local/bin/wifi_rebooter.sh

    #!/bin/bash
	
	# The IP for the server you wish to ping (8.8.8.8 is a public Google DNS server)
	SERVER=8.8.8.8

	# Only send two pings, sending output to /dev/null
	ping -c2 ${SERVER} > /dev/null

	# If the return code from ping ($?) is not 0 (meaning there was an error)
	if [ $? != 0 ]
	then
	    # Restart the wireless interface
	    ifdown --force wlan0
	    ifup wlan0
	fi
```

```
chmod +x /usr/local/bin/wifi_rebooter.sh
```

```
sudo nano /etc/crontab
```

add the line:

```
30 *	* * *	root	/usr/local/bin/wifi_rebooter.sh
```


