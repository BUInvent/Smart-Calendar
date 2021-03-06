import os, sys, serial, time

option = str(sys.argv[1:2])

if(option == '[\'--start\']'):
	#create communication file
	if(not os.path.isfile('/var/www/Smart-Calendar/HTML/temporary/message.txt')):
		file = open('/var/www/Smart-Calendar/HTML/temporary/message.txt', 'w+')
		file.close()
	#create timestamp file
	if(not os.path.isfile('/var/www/Smart-Calendar/HTML/temporary/stamp.txt')):
		file = open('/var/www/Smart-Calendar/HTML/temporary/stamp.txt', 'w+')
		file.write('File Created ' + time.asctime() + '\n')
		file.close()
	#turn on pins, set to input
	os.system("echo 17 > /sys/class/gpio/export")
	os.system("echo in > /sys/class/gpio/gpio17/direction")
	os.system("echo 27 > /sys/class/gpio/export")
	os.system("echo in > /sys/class/gpio/gpio27/direction")
	os.system("python /var/www/Smart-Calendar/Background/pins.py &")

elif(option == '[\'--stop\']'):
	os.system("kill $(ps -eF | grep pins.py | grep -v grep | awk '{print $2}')") #end pins.py
	os.system("kill $(ps -eF | grep firefox | grep -v grep | awk '{print $2}')") #end firefox
	#turn off pins
	os.system("echo 17 > /sys/class/gpio/unexport")
	os.system("echo 27 > /sys/class/gpio/unexport")
	#format timestamp file
	timevar = time.asctime()
	file = open('/var/www/Smart-Calendar/HTML/temporary/stamp.txt', 'a+')
	file.write('File Closed ' + timevar + '\n')
	file.close()
	timevar = timevar[4:7] + '_' + timevar[8:10] + '_' + timevar[20:] + '_stamp.txt'
	os.rename("/var/www/Smart-Calendar/HTML/temporary/stamp.txt", "/var/www/Smart-Calendar/HTML/temporary/" + timevar)
	#email file

elif(option == '[\'--monitor-on\']'):
	os.system("tvservice -p; chvt 6; chvt 7") #turn on hdmi port
	#close power to monitor through serial
	ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
	code = 'A00101A2'
	ser.write(code.decode('HEX'))

elif(option == '[\'--monitor-off\']'):
	os.system("tvservice -p; tvservice -o") #turn off hdmi port
	#open power to monitor through serial
	ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
	code = 'A00100A1'
	ser.write(code.decode('HEX'))
	
