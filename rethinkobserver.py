# -*- coding: utf-8 -*-

##
## Monitoring system for SmartPoliTech
##
## Bridge code that writes metrics to INFLUXDB as soon as they arrive to RETHINKDB, using the change function
##
## July 2016 - Pablo Bustos
## Marzo 2017 - Agustín
##

import sys, json, requests, time, pprint
from PySide.QtCore import *
import rethinkdb as rdb
import datetime as dt
from rethinkreader import RDBReader
from dateutil import parser
from influxdb import InfluxDBClient
from subprocess import call
import ConfigParser

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


rethinkIP = "158.49.247.126"
rethinkDB = "smartpolitech"
influxIP = "10.253.247.18"
influxDB = "sensors"		

#if has a config file in argument read this
if (len(sys.argv)==2):
	configFilePath = sys.argv[1]
	configParser = ConfigParser.RawConfigParser()   
	configParser.read(configFilePath)
	rethinkIP = configParser.get('config', 'rethinkIP')
	rethinkDB = configParser.get('config', 'rethinkDB')
	influxIP = configParser.get('config', 'influxIP')
	influxDB = configParser.get('config', 'influxDB')	
	
connDataRETHINK = {"host": rethinkIP, "port": "28015", "db": rethinkDB, "auth_key": ""}

#class MainWindow(QMainWindow, Ui_MainWindow):
class Main():
	def __init__(self):
		# open connection to RETHINKDB
		self.conn = rdb.connect(host=connDataRETHINK["host"], port=connDataRETHINK["port"], db=connDataRETHINK["db"])

		self.reader = RDBReader(connDataRETHINK)
		self.reader.start()

		devices = rdb.table("devices").run(self.conn)
		for device in list(devices):
			table = device["id"]
			if rdb.table(table).is_empty().run(self.conn) is False:
				datos = rdb.table(table).order_by(index=rdb.desc('created_at')).limit(1).run(self.conn)
			self.reader.addTable(table)

		self.reader.signalVal.connect(self.slotFromReader)

	# Slot that is called from Tornado readers to notify that a new data has arrvied
	@Slot(str)
	def slotFromReader(self, table, measure):
		datos = table + " "

		for k, v in measure['data'].iteritems():
			v = str(v).replace(',','.')
			if is_number(v):
				datos += k + "=" + v + ","				
		
		datos = datos[:-1]
		cabecerahttp = "http://" + influxIP + ":8086/write?db=" + influxDB
		print "curl -i -POST " + cabecerahttp + "-u admin:alwayssmarter --data-binary " + datos
		#print call(["curl", "-i", "-POST", cabecerahttp, "-u", "admin:alwayssmarter", "--data-binary", datos])

if __name__ == '__main__':
	app = QCoreApplication(sys.argv)
	mainWin = Main()
	ret = app.exec_()
	sys.exit(ret)
