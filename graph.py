from shape import *
import matplotlib.pyplot as plt

class Graph():
	def __init__(self):
		self.map = None
		self.dest = None
		self.start = None
		self.path = None

	def set_graph(self, tmp_map):
		self.map = tmp_map

	def set_dest(self,dest):
		self.dest = dest

	def set_start(self,start):
		self.start = start

	def locate_node(self,pos):
		for key,node in self.map.items():
				inside,loc = p_inside_rect(pos,node.shape)

				if inside == True:
					return key
		return None
	
	def reset_nodes(self):
		for key, node in self.map.items():
			node.visited = False
			node.prev = None

	def dijkstras(self):
		print("inside dijkstras")
		self.reset_nodes()
		cost = dict((el,float("inf")) for el in self.map.keys())
		queue = [self.start]
		cost[self.start] = 0
		visited = [self.start]

		while len(queue) > 0:
			node = queue.pop(0)
			visited.append(node)
			nodes = self.map[node].neighbors_pos()
			for n in nodes:
				if cost[n] > cost[node] + length(node,n):
					self.map[n].prev = node
				cost[n] = min(cost[n],cost[node]+length(node,n))
				if n not in visited:
					queue.append(n)
		#print(cost)
		#print(self.map[self.dest].prev)
		node = self.dest
		path = []
		while node != None:
			path.append(node)
			node = self.map[node].prev
		return path[::-1]

	def distance_to_dest(self,pos):
		return length(self.dest,pos)

	def a_star(self):
		print("inside a_star")
		self.reset_nodes()

		#G value is the cost form start to current node
		costG = dict((el,float("inf")) for el in self.map.keys())
		#H estimated cost from current to goal
		costH = dict((el,float("inf")) for el in self.map.keys())
		#F = G + H
		costF = dict((el,float("inf")) for el in self.map.keys())

		costG[self.start] = 0
		costH[self.start] = self.distance_to_dest(self.start)
		costF[self.start] = costG[self.start] + costH[self.start]

		min_node = self.start
		visited = []

		print("costG:")
		print(costG)
		print('costH:')
		print(costH)

		while(min_node):
			node = min_node
			min_node = None
			visited.append(node)

			#update G cost and H cost around neighbors
			nodes = self.map[node].neighbors_pos()
			print("a_star neighbors: "+ str(nodes))
			for n in nodes:
				dd = self.distance_to_dest(n)
				#destination is reached
				if(dd == 0):
					print("break inside a_star")
					self.map[n].prev = node
					break;

				costH[n] = dd	
				dist_to_node = costG[node] + length(node,n) 
				if(costG[n] > dist_to_node):
					costG[n] = dist_to_node
					self.map[n].prev = node

				#update F
				costF[n] = costG[n] + costH[n]

			#determine the next min
			candidates = sort_eliminate_key(costF,visited)
			print("a_star: candidate: " + str(candidates))
			if(len(candidates) > 0):
				min_node = candidates[0]

			print("a_star: explored "+str(node))
			print("a_star: Fcost: ")
			print(costF)
			print("a_star: next: " + str(min_node))

		node = self.dest
		path = []
		while node != None:
			path.append(node)
			node = self.map[node].prev
		return path[::-1]	


	# a wonderfully clear path
	def tree_extend(self,branch):
		if self.map == None:
			init = branch[0]
			self.map = dict()
			self.map[init] = Node(init[0], init[1])
			print("tree initialized: " + str(self.map.keys()))

		#start branch with a known position
		p = branch.pop(0)
		assert(p in self.map.keys())
		
		#extend branch
		while len(branch) > 0:
			node = branch.pop(0)
			if node not in self.map.keys():
				self.map[node] = Node(node[0],node[1])
			self.map[node].prev = p
			p = node

	#print tree structure
	def print_tree(self):
		for node in self.map.keys():
			prev = self.map[node].prev
			if prev:
				print(str(node) + "--" + str(prev))
			else:
				print(str(node) + "-- None")

	#closest distance based on euclean distance
	def closest_point(self,pos):
		closest_point = self.map.keys()[0]
		distance = (closest_point[0]-pos[0])**2 + (closest_point[1]-pos[1])**2
		for k in self.map.keys():
			dist = (k[0] - pos[0])**2 + (k[1] - pos[1])**2
			if (dist < distance):
				closest_point = k
				distance = dist
		return closest_point

	def traceback(self):
		assert(self.start != None)
		assert(self.dest != None)

		node = self.dest
		if(node not in self.map.keys()):
				print("failed to traceback")
				return []

		path = []
		while node != None:
			path.append(node)
			node = self.map[node].prev
			
		self.path = path[::-1]
		return self.path	

	def graph_print(self):
		points = self.map.keys()
		x = []
		y = []
		edgex = []
		edgey =  []

		for (i,j) in self.map.keys():
			plt.plot([i],[j],'ro')
			if(self.map[(i,j)].prev):
				(prev_i,prev_j) = self.map[(i,j)].prev
				plt.plot([prev_i,i],[prev_j,j],'k')
		
		if(self.path):
			prev = self.path[0]
			for(i,j) in self.path:
				plt.plot([i,prev[0]],[j,prev[1]],color="y",linewidth=2)
				prev = (i,j)
		plt.title('Path Graph')
		plt.show()





def sort_eliminate_key(d,visited):
	l = {}
	for i in d.items():
		if i[1] < float("inf") and i[0] not in visited:
			l[i[0]] = i[1]
	return sorted(l,key=lambda k:l[k])



class Node():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.neighbors = dict(up=None,down=None,left=None,right=None)
			#q1=None,q2=None,q3=None,q4=None)
		self.shape = None
		self.visited = False
		self.prev = None

	def __eq__(self, other):
		if isinstance(other, Node):
			return self.x == other.x and self.y == other.y
	#print function
	def __repr__(self):
		s = "center (x,y): ("+str(self.x)+" "+str(self.y) + ")\n" + "visited: "+str(self.visited)+"\n"
		s += "-----neighbor information------\n"
		s += "empty neighbors: " + str(self.empty_neighbors()) + "\n"
		for n in self.neighbors.keys():
			if self.neighbors[n] is not None:
				s+= n +"'s empty neighbors: " + str(self.neighbors[n].empty_neighbors()) + "\n"
		s +="\n------------------------------\n"
		return s
	
	def get_pos(self):
		return (self.x,self.y)

	#node should be a position tupple
	def set_prev(self,node):
		self.prev = node

	def set_shape(self,shape):
		self.shape = shape
	
	def get_dim(self):
		if self.shape is None:
			print("need shape for this node")
			return
		return (self.shape.get_width(),self.shape.get_height())

	#input: rp: string, relative position | n: neighboring node
	def assign_neighbor(self,rp,n):
		assert(n != None)
		assert(rp in self.neighbors.keys())
		self.neighbors[rp] = n


	#return all neighbors unexplored
	def empty_neighbors(self):
		unexplored = []
		for k in self.neighbors.keys():
			if self.neighbors[k] is None:
				unexplored.append(k)
		return unexplored

	#return all neighbors that are explored
	def neighbors(self):
		explored = []
		for k in self.neighbors.keys():
			if self.neighbors[k]:
				explored.append((k,self.neighbor(k)))
		return explored

	def neighbors_pos(self):
		explored = []
		for k,node in self.neighbors.items():
			if node:
				explored.append(node.get_pos())
		return explored

