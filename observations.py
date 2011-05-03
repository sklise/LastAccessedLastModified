#!/usr/bin/python

import urllib
from xml.dom import minidom

### Observations
zipcode = "10003"

### Weather data
wurl = "http://xml.weather.yahoo.com/forecastrss?p="+zipcode+"&u=f";
r = minidom.parse(urllib.urlopen(wurl)) # open each url as a dom element
lat = r.getElementsByTagName('geo:lat')[0].firstChild.nodeValue
lon = r.getElementsByTagName('geo:long')[0].firstChild.nodeValue
conditions = r.getElementsByTagName('yweather:condition')[0]

### File Info

### Context Free Grammars => For when we aren't anywhere

### Save Zipcodes in a dicitonary
zipcodes = dict()
zips = open('shortzips.txt')
for line in zips:
	line = line.strip()
	bits = line.split(",")
	# print bits[1].strip('"')
	zipcodes[int(bits[1].strip('"'))] = bits[3].strip('"')

class Observe(object):
	
	def __init__(self):
		self.output = ""
	
	def wearehere(self,loc):
		import random
		
		if loc != int(zipcode):
			self.output += "This is not "+zipcodes[int(loc)]+"\n"
			self.wearehere(random.choice(zipcodes.keys()))
		else:
			self.output += "We are in "+zipcodes[int(zipcode)]+"\n"


if __name__ == '__main__':
	poem = Observe()
	poem.wearehere(11222)
	print poem.output
