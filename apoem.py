#!/usr/bin/python
import urllib
from xml.dom import minidom
import os, stat, random
from datetime import datetime

### Observations
zipcode = "10003"

### Context Free Grammars => For when we aren't anywhere
class ContextFree(object):
	import random
	"""Rules for a context free grammar."""
	def __init__(self):
		self.rules = dict()
		self.expansion = list()
		
	def addRule(self, rule, expansion):
		"""Specify a symbol and then that symbol's expansion"""
		if rule in self.rules:
			self.rules[rule].append(expansion)
		else:
			self.rules[rule] = [expansion]
			
	def expand(self, start):
		"""If start is a rule, expand it, run expand again, else append it to the output"""
		if start in self.rules:
			expansions = self.rules[start]
			exchoice = random.choice(expansions)
			for w in exchoice:
				self.expand(w)
		else:
			self.expansion.append(start)
			
	def makegrammar(self,base):
		self.expand(base)
		return self.expansion
		

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
		self.fileinfo("/Users/sklise/ITP/S11_RWET/Observations")
		self.output = ""
	
	### File Info # http://leiqing.org/mirrors/python-2.7.1-docs-html/library/stat.html
	def fileinfo(self,filepath):
		st = os.stat(filepath)
		accessed = datetime.fromtimestamp(st.st_atime)
		modified = datetime.fromtimestamp(st.st_mtime)
		self.groupread = bool(st.st_mode & stat.S_IRGRP) # Group has read permission.
		self.groupwrite = bool(st.st_mode & stat.S_IWGRP) # Group has write permission.
		self.groupexecute = bool(st.st_mode & stat.S_IXGRP) # Group has execute permission.
	
	def uptime(self):
		try:
			### If the computer has been up longer than a day, things change.
			os.system("uptime > uptime.txt")
			f = open("uptime.txt")
			contents = f.read().split()
			f.close()
			return contents[2]+" day and "+contents[4][2:];
		except:
			return "way too many"
	
	### Weather data
	def weather(self,loc):
		wurl = "http://xml.weather.yahoo.com/forecastrss?p="+str(loc)+"&u=f";
		r = minidom.parse(urllib.urlopen(wurl)) # open each url as a dom element
		self.condition = r.getElementsByTagName('yweather:condition')[0].getAttribute("text")
		self.sunrise = r.getElementsByTagName('yweather:astronomy')[0].getAttribute("sunrise")
		self.sunset = r.getElementsByTagName('yweather:astronomy')[0].getAttribute("sunset")
	
	def whichcity(self,loc):
		
		if loc != int(zipcode):
			self.output += "This is not "+zipcodes[int(loc)]+"\n"
			try: 
				self.weather(loc)
				if random.random() < .5:
					self.output += "    It would be "+self.condition+"\n"
				else:
					self.output += "    There the sun rises at"+self.sunrise+"\n"
			except:
				self.output +="\n"
			self.whichcity(random.choice(zipcodes.keys()))
		else:
			self.output += "Here we are in "+zipcodes[int(zipcode)]+"\n"
			try:
				self.weather(loc)
				self.output += "    But the sun set at "+self.sunset+"\n"
			except:
				self.output += "\n"
	
	def who(self):
		try:
			os.system("whoami>user.txt")
			f = open("user.txt")
			self.user = f.read().strip()
			f.close()
			return self.user
		except:
			return "\n"
	

if __name__ == '__main__':
	poem = Observe()
	c = ContextFree()
	# I = intro {}
	c.addRule('I',['GP'])
	c.addRule('GP',['Hi','GP'])
	c.addRule('GP',['Hello','GP'])
	c.addRule('GP',['Good Evening\n','G'])
	c.addRule('GP',[poem.who(),'G'])
	c.addRule('G',['I wrote','G'])
	c.addRule('G',['this','G'])
	c.addRule('G',['this is a poem\n','U'])
	c.addRule('U',['I\'ve been awake for',poem.uptime(),'hours','T','\n'])
	c.addRule('U',['It\'s been',poem.uptime(),' hours\n','T','\n'])
	c.addRule('T',['It will be great'])
	c.addRule('T',['The poem might','TR'])
	c.addRule('TR',['sound funky.\n'])
	c.addRule('TR',['inspire you.\n'])
	c.addRule('TR',['revolutionize.\n'])
	c.makegrammar('GP')
	print ' '.join(c.expansion)
	poem.whichcity(11222)
	print poem.output