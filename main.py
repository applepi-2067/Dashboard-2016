import cherrypy
from threading import Thread
from networktables import NetworkTable
from time import sleep
import logging
import configparser

robot = 'roborio-2067-frc.local'

print("initializing")

logging.basicConfig(level=logging.DEBUG)
config = configparser.ConfigParser()

NetworkTable.setIPAddress(robot)
NetworkTable.setClientMode()
NetworkTable.initialize()

sd = NetworkTable.getTable('SmartDashboard')
print("waiting for robot at: " + robot)

class ScoutServer(object):
	@cherrypy.expose
	def index(self, COG_X="", COG_Y=""):
		if sd.isConnected():
			sd.putNumber("COG_X", COG_X)
			sd.putNumber("COG_Y", COG_Y)
		return COG_X
		
conf = {
	'global': {
		'server.socket_port': 8000
	}
}

def start():
	cherrypy.quickstart(ScoutServer(), '/', conf)
	
Thread(target=start).start() #launch http server in separate thread

while not sd.isConnected():
	sleep(0.1)

print("now connected")

n = 0
while True:
	n += 1
	print("Config iteration " + str(n))
	config.read("robot2016.ini")
	for section in config.sections():
		for key in list(config[section].keys()):
			val = config[section][key]
			try:
				val = float(val)
			except:
				print("something broke")
			
			print("Loading: " + section + "/" + key + ": " + str(val))
			sd.putNumber(section + '/' + key, val)
	sleep(1.5)