

class Node():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.neighbors = dict(up=None,down=None,left=None,right=None,
			q1=None,q2=None,q3=None,q4=None)
		self.shape = None
		self.visited = False

	def __eq__(self, other):
		if isinstance(other, Node):
			return self.x == other.x and self.y == other.y
	#print function
	def __repr__(self):
		s = "center (x,y): ("+str(self.x)+" "+str(self.y) + ")\n" + "visited: "+str(self.visited)+"\n"
		s += "-----neighbor information------\n"
		s += "unexplored: " + str(self.unexplored_neighbors()) + "\n"
		for n in self.neighbors.keys():
			if self.neighbors[n] is not None:
				s+= n +"'s information: " + str(self.neighbors[n].unexplored_neighbors()) + "\n"
		s +="\n------------------------------\n"
		return s

	def set_shape(self,shape):
		self.shape = shape
	
	def get_dim(self):
		if self.shape is None:
			print("need shape for this node")
			return
		return (self.shape.get_width(),self.shape.get_height())

	#return all neighbors unexplored
	def unexplored_neighbors(self):
		unexplored = []
		for k in self.neighbors.keys():
			if self.neighbors[k] is None:
				unexplored.append(k)
		return unexplored

	#return all neighbors that are explored
	def explored_neighbors(self):
		explored = []
		for k in self.neighbors.keys():
			if self.neighbors[k]:
				explored.append((k,self.neighbor(k)))
		return explored

