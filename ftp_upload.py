
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


from ftplib import FTP
#from time import sleep

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

    

