#! /usr/bin/env python

import json
import os
from pprint import pprint, pformat
import sqlite3
import sys
import time
import urllib
import urllib2
import wmatacredentials

def do_wmata_call():
	url = 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/All'
	headers = {'api_key': wmatacredentials.primarykey}

	try:
		success = True
		request = urllib2.Request(headers = headers, url = url)
		requestFile = urllib2.urlopen(request)
	except urllib2.HTTPError, e:
		print "Error making WMATA call %s: (%i) %s" % (url, e.code, e.reason)
		return None

	rawdata = requestFile.read()
	try:
		result = json.loads(rawdata)
	except:
		return None
	return result

def createTables(db):
	tableSQL = """CREATE TABLE data(Time, Car, Destination, DestinationCode, DestinationName, `Group`, Line, LocationCode, LocationName, Min);"""
	table2SQL = """CREATE TABLE rawdata(time, raw);"""
	try:
		db.execute(tableSQL);
		db.execute(table2SQL);
		db.commit();
	except:
		pass


def main():
	try:
		filename = sys.argv[1]
	except:
		filename = None

	if not filename:
		print "Database filename required."
		return None

	try:
		db = sqlite3.connect(filename)
	except Exception, e:
		print "Error opening database: %s" % pformat(e)
		return None
	
	createTables(db)

	insertSQL = """INSERT INTO data(Time, Car, Destination, DestinationCode, DestinationName, `Group`, Line, LocationCode, LocationName, Min) VALUES(DATETIME('now'), :Car, :Destination, :DestinationCode, :DestinationName, :Group, :Line, :LocationCode, :LocationName, :Min);"""

	data = do_wmata_call()

	if not data:
		return False

	db.execute("INSERT INTO rawdata(time, raw) VALUES(DATETIME('now'), :data);", {"data": pformat(data)})
	db.commit();
	db.executemany(insertSQL, data['Trains'])
	db.commit();

main()
