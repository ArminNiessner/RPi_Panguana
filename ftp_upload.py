from ftplib import FTP
#from time import sleep

def ftp_upload():
    server = 'ftp.taysira.org'
    username = 'aniessner@taysira.org'
    password = 'e2m3f4meA?'

    try:
        ftp_connection = FTP(server, username, password)
        fh = open("/home/pi/Desktop/datalog_pi.csv", 'rb')
        ftp_connection.storbinary('STOR datalog_pi.csv', fh)
        fh.close()
    except FileNotFoundError:
        pass

    

