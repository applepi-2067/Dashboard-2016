from networktables import NetworkTable
from time import sleep
#import logging
import configparser

robot = 'roborio-2067-frc.local'

print("initializing")

config = configparser.ConfigParser()
config.read("robot2015.ini")

#logging.basicConfig(level=logging.DEBUG)

NetworkTable.setIPAddress(robot)
NetworkTable.setClientMode()
NetworkTable.initialize()

sd = NetworkTable.getTable('SmartDashboard')
print("waiting for robot at: " + robot)

while not sd.isConnected():
	sleep(0.1)

print("now connected")

for section in config.sections():
	for key in list(config[section].keys()):
		print("loading: " + section + '-' + key)
		val = config[section][key]
		try:
			val = float(val)
		except:
			pass
			
		sd.putNumber(section + '-' + key, val)

print("config loaded")
t = 0
print("now listening for robot diagnostics")
with open('Robot Logs/diag.csv', 'a') as f:
	while True:
		l = 0
		r = 0
		try:
			l = sd.getNumber('Left Wheel')
			r = sd.getNumber('Right Wheel')
		except:
			print('something broke')
		f.write(str(round(t, 3)) + ',' + str(l) + ',' + str(r) + '\n')
		t += 0.05
		sleep(0.05)