#!/usr/bin/python

import urllib
from xml.dom import minidom
import os
import stat


### Observations
zipcode = "10003"

### File Info
# http://leiqing.org/mirrors/python-2.7.1-docs-html/library/stat.html
def isgroupreadable(filepath):
  st = os.stat(filepath)
  return bool(st.st_mode & stat.S_IWGRP)

### Context Free Grammars => For when we aren't anywhere

### Save Zipcodes in a dicitonary
zipcodes = dict()
zips = open('shortzips.txt')
for line in zips:
	line = line.strip()
	bits = line.split(",")
	zipcodes[int(bits[1].strip('"'))] = bits[3].strip('"')

### Obseerve class:: Where the poem is written.
class Observe(object):
	
	def __init__(self):
		self.output = ""
	
	def weather(self,loc):
		### Weather data
		wurl = "http://xml.weather.yahoo.com/forecastrss?p="+str(loc)+"&u=f";
		r = minidom.parse(urllib.urlopen(wurl)) # open each url as a dom element
		# lat = r.getElementsByTagName('geo:lat')[0].firstChild.nodeValue
		# lon = r.getElementsByTagName('geo:long')[0].firstChild.nodeValue
		self.condition = r.getElementsByTagName('yweather:condition')[0].getAttribute("text")
		self.sunrise = r.getElementsByTagName('yweather:astronomy')[0].getAttribute("sunrise")
	
	def whichcity(self,loc):
		import random
		
		if loc != int(zipcode):
			self.output += "This is not "+zipcodes[int(loc)]+"\n"
			try: 
				self.weather(loc)
				self.output += "    It would be "+self.condition+"\n"
				self.output += "    Sunrise "+self.sunrise+"\n"
			except:
				self.output +="\n"
			self.whichcity(random.choice(zipcodes.keys()))
		else:
			self.output += "We are in "+zipcodes[int(zipcode)]+"\n"

if __name__ == '__main__':
	print isgroupreadable("/Users/sklise/ITP/S11_RWET/Observations")
	poem = Observe()
	poem.whichcity(11222)
	print poem.output
