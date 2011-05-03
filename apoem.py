#!/usr/bin/python
import urllib
from xml.dom import minidom
import os
import stat
from datetime import datetime

### Observations
zipcode = "10003"

### File Info
# http://leiqing.org/mirrors/python-2.7.1-docs-html/library/stat.html
def fileinfo(filepath):
	st = os.stat(filepath)
	print st
	min = 60
	hour = min*60
	day = hour*24
	accessed = datetime.fromtimestamp(st.st_atime)
	modified = datetime.fromtimestamp(st.st_mtime)
	print "Last accessed: "+str(accessed)
	print "I finished writing this at: "+str(modified)
	print bool(st.st_mode & stat.S_IRGRP) # Group has read permission.
	print bool(st.st_mode & stat.S_IWGRP) # Group has write permission.
	print bool(st.st_mode & stat.S_IXGRP) # Group has execute permission.

def uptime():
	try:
		os.system("uptime > uptime.txt")
		f = open("uptime.txt")
		contents = f.read().split()
		f.close()
		return contents[2].split(":")[0];
	except:
		return "way too long"

print "The system uptime is:", uptime()

### Context Free Grammars => For when we aren't anywhere


### Save Zipcodes in a dicitonary
zipcodes = dict()
zips = open('shortzips.txt')
for line in zips:
	line = line.strip()
	bits = line.split(",")
	zipcodes[int(bits[1].strip('"'))] = bits[3].strip('"')

### Observe class:: Where the poem is written.
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
		self.sunset = r.getElementsByTagName('yweather:astronomy')[0].getAttribute("sunset")
	
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
			try:
				self.weather(loc)
				self.output += "    But the sun set at "+self.sunset+"\n"
			except:
				self.output += "\n"

if __name__ == '__main__':
	fileinfo("/Users/sklise/ITP/S11_RWET/Observations")
	poem = Observe()
	poem.whichcity(11222)
	print poem.output
