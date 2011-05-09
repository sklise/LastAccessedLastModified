#!/usr/bin/python
import urllib
from xml.dom import minidom
import os, stat, random
from datetime import datetime

#
# Last Accessed Last Modified
# Steven Klise <http://stevenklise.com>
# Reading & Writing Electronic Text, 2011 <http://rwet.decontextualize.com>
# Much help from Adam Parrish <http://decontextualize.com>
#

### Where is the computer?
zipcode = "10003"
### Where is this file?
filepath = "/Users/sklise/ITP/S11_RWET/LastAccessedLastModified/apoem.py"

### Context Free Grammars
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
	"""What can the computer perceive of its surroundings?"""
	def __init__(self):
		self.fileinfo(filepath)
		self.output = ""
	
	### File Info # http://leiqing.org/mirrors/python-2.7.1-docs-html/library/stat.html
	def fileinfo(self,filepath):
		st = os.stat(filepath)
		self.accessed = datetime.fromtimestamp(st.st_atime)
		self.modified = datetime.fromtimestamp(st.st_mtime)
		self.groupread = bool(st.st_mode & stat.S_IRGRP) # Group has read permission.
		self.groupwrite = bool(st.st_mode & stat.S_IWGRP) # Group has write permission.
		self.groupexecute = bool(st.st_mode & stat.S_IXGRP) # Group has execute permission.

	def access(self):
		return "> Last accessed "+str(self.accessed)
		
	def read(self):
		return "> Last modified "+str(self.modified)
	
	def uptime(self):
		try:
			### If the computer has been up longer than a day, things change.
			os.system("uptime > uptime.txt")
			f = open("uptime.txt")
			contents = f.read().split()
			f.close()
			return contents[2]+" day and "+contents[4][:2];
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
			self.output += "# This is not "+zipcodes[int(loc)]+"\n"
			try: 
				self.weather(loc)
				if random.random() < .5:
					if random.random() < .5:
						self.output += "    It would be "+self.condition+"\n"
					else:
						self.output += "    "+self.condition+" would be the weather.\n"
				else:
					if random.random() < .5:
						self.output += "    There the sun rises at "+self.sunrise+".\n"
					else:
						self.output += "    Their sun will rise at "+self.sunrise+".\n"
			except:
				self.output +="\n"
			self.whichcity(random.choice(zipcodes.keys()))
		else:
			self.output += "# Here we are in "+zipcodes[int(zipcode)]+"\n"
			try:
				self.weather(loc)
				self.output += "    It will get dark at "+self.sunset+"\n"
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
	poem.output += poem.access()+"\n"
	
	c.addRule('I',['GP'])
	c.addRule('GP',['# login:\nHi','GP'])
	c.addRule('GP',['# login:\nHello','GP'])
	c.addRule('GP',['# login:\nGood Evening\n','G'])
	c.addRule('G',['I wrote','G'])
	c.addRule('G',['this','G'])
	c.addRule('G',['this is a poem\n','U'])
	c.addRule('U',['This computer has been awake for',poem.uptime(),'hours','T','\n'])
	c.addRule('U',['It\'s been',poem.uptime(),' hours\n','T','\n'])
	c.addRule('T',['The poem might','TR'])
	c.addRule('TR',['be '+str(int(random.random()*15))+' lines.\n'])
	c.addRule('TR',['consume '+str(int(random.random()*400))+' processes.\n'])
	c.makegrammar('GP')
	print ' '.join(c.expansion)
	poem.whichcity(11222)
	
	poem.output += poem.read()
	
	print poem.output