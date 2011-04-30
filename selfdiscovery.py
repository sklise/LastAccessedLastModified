class SelfDiscovery(object):
	
	def __init__(self):
		self.ip = tuple() # [X,X,X,X]
		self.inittime = dict() # {year,month,date,hour,minute}
		self.lastmod = dict() # {year,month,date,hour,minute}
		self.permissions = dict() # {user,group,other}
		self.git = dict() # {commit,count}
		
