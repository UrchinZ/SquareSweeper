

class Node():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.neighbors_status = dict(up=False,down=False,left=False,right=False,
			q1=False,q2=False,q3=False,q4=False)
		self.neighbors = dict(up=None,down=None,left=None,right=None,
			q1=None,q2=None,q3=None,q4=None)
	
	#print function
	def __repr__(self):
		s = "center (x,y): ("+str(self.x)+" "+str(self.y) + ")\n"
		s += "=====neighbor status=====\n"+str(self.neighbors_status) + "\n------------------------\n"
		s += "-----neighbor information------\n" + str(self.neighbors)+"\n========================\n"
		return s

	#set neighbor explored
	def set_neighbor_explored(self,n,origin):
		self.neighbors_status[n] = True
		self.neighbor[n] = origin

	#return all neighbors unexplored
	def unexplored_neighbors(self):
		unexplored = []
		for k in self.neighbors_status.keys():
			if not self.neighbors_status[k]:
				unexplored.append(k)
		return unexplored

	#return all neighbors that are explored
	def explored_neighbors(self):
		explored = []
		for k in self.neighbors_status.keys():
			if not self.neighbors_status[k]:
				explored.append((k,self.neighbor(k)))
		return explored

