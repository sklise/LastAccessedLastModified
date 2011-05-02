#!/usr/bin/python

import urllib
from xml.dom import minidom

### Observations
zipcode = "11222"

### Weather data
wurl = "http://xml.weather.yahoo.com/forecastrss?p="+zipcode+"&u=f";
r = minidom.parse(urllib.urlopen(wurl)) # open each url as a dom element
lat = r.getElementsByTagName('geo:lat')[0].firstChild.nodeValue
lon = r.getElementsByTagName('geo:long')[0].firstChild.nodeValue
conditions = r.getElementsByTagName('yweather:condition')[0]
### Twitter feed

###

### Save Zipcodes in a dicitonary
zipcodes = dict()
zips = open('zips.txt')
for line in zips:
	line = line.strip()
	bits = line.split(",")
	# print bits[1].strip('"')
	zipcodes[int(bits[1].strip('"'))] = bits[3].strip('"')


def wearehere(self, loc):
	import random
	
	output = ""
	
	if loc is not zipcode:
		output += "This is not "+zipcodes[int(loc)]+"\n"
		self.wearehere(random.choice(zipcodes))
	else:
		output+= "We are in "+zipcodes[int(zipcode)]+"\n"
		return self.output
		
weareheare(11222)
