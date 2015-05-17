#! /usr/bin/env python

import json
from pprint import pprint
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

def main():
	data = do_wmata_call()

	if not data:
		return False

	pprint(data)

main()
