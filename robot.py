import pyglet, time
from pyglet.window import mouse
from pyglet.window import key
from actor import Actor
from shape import *
from graph import *

#specialized actor robot
class SquareRobot(Actor):
	def __init__(self):
		DIM = (50,50)
		center = (25,25)
		self.sensor = None
		v1 = V(center[0]-DIM[0]/2, center[1]-DIM[1]/2)
		#v2 = V(center[0]-DIM[0]/2, center[1]+DIM[1]/2)
		#v3 = V(center[0]+DIM[0]/2, center[1]+DIM[1]/2)
		#v4 = V(center[0]+DIM[0]/2, center[1]-DIM[1]/2)
		#self.parts = [Polygon([v1,v2,v3,v4])]
		self.parts = [Rectangle(v1,width = DIM[0],height=DIM[1])]
		self.actor_type = "robot"
		#self.key_handler = key.KeyStateHandler()
		#self.event_handlers = [self, self.key_handler]
		self.speed = 2
		self.keys = dict(left=False, right=False, up=False, down=False, dijk = False)
		self.dest = []
		self.map = None

	def set_sensor(self,sensor):
		self.sensor = sensor

	def get_dim(self):
		return (self.parts[0].get_width(),self.parts[0].get_height())

	def on_key_press(self, symbol, modifiers):
		if symbol == key.SPACE:
			print("space presed")
		elif symbol == key.UP:
			print("up")
			self.keys["up"] = True
		elif symbol == key.DOWN:
			print("down")
			self.keys["down"] = True
		elif symbol == key.RIGHT:
			print("right")
			self.keys["right"] = True
		elif symbol == key.LEFT:
			print("left")
			self.keys["left"] = True
		elif symbol == key.D:
			print("Running dijk's...")
			self.keys["dijk"] = True


	def on_key_release(self, symbol, modifiers):
		if symbol == key.UP:
			print("release up")
			self.keys['up'] = False
		elif symbol == key.DOWN:
			print("release down")
			self.keys['down'] = False
		elif symbol == key.LEFT:
			print("release left")
			self.keys['left'] = False
		elif symbol == key.RIGHT:
			print("release right")
			self.keys['right'] = False


	def update(self,dt,DIM,actors):
		#print("update in robot " + str(dt))
		if self.keys['up']:
			self.move((0,1*self.speed),DIM,actors)
		if self.keys['down']:
			self.move((0,-1*self.speed),DIM,actors)
		if self.keys['left']:
			self.move((-1*self.speed,0),DIM,actors)
		if self.keys['right']:
			self.move((1*self.speed,0),DIM,actors)
		if self.keys['dijk']:
			self.dijk()

	def dijk(self):
		if (len(self.dest) == 0):
			print("exiting dijkstra function")
			return
		if (self.sensor == None):
			print("do not have sensor")
			return

		print("I need to do some dijkstra stuff")
		if not self.map:
			self.construct_belief_map()

		else:
			print("running to destinations:")
			print(self.dest)

		while len(self.dest):
			time.sleep(2)
			destination = self.dest.pop(0)

		self.keys['dijk'] = False


	def on_mouse_press(self, x, y, button, modifiers):
		if button == 1:
			#pyglet doesn't respond to clicks outside the stage
			self.dest.append(V(x,y))
			#I might want to sort dest
			print(self.dest)

	#run bfs to construct a reasonable map
	def construct_belief_map(self):
		my_center = self.parts[0].get_center()
		dim = self.get_dim()
		queue = [(my_center.x,my_center.y)]
		visited_nodes = {}
		while(len(queue)>0):
			pos = queue.pop(0)
			neighbor_list = generate_neighbors(pos,dim,self.sensor)
			for neighbor in neighbor_list:
				if neighbor not in queue and neighbor not in visited_nodes.keys():
					queue.append(neighbor)
			#mark position in visited node
			visited_nodes[pos] = None
		print("queue: ")
		print(queue)
		print(len(queue))
		print("visited_nodes:")
		print(visited_nodes)
		print(len(visited_nodes.keys()))


		'''
		i = Node(my_center.x,my_center.y)
		i.set_shape(self.parts[0])
		print(i)
		#bfs queue
		queue = [i]
		visited_nodes = []
		print("before generate neighbors")
		generate_neighbors(i,self.sensor)
		limit = 30
		while len(queue) > 0:
			node = queue.pop(0)
			connect_nodes(node)
			visited_nodes.append(node)
			generate_neighbors(node,self.sensor)
			node.visited = True
			print("exploring:")
			print(node)
			print("###########block of death##########")
			order = ["q2","up","q1","right","q3","down","q4","left"]
			for n in order:
				print(n)
				if node.neighbors[n] is not None:
					if(node.neighbors[n].visited):
						#print(node.neighbors[n])
						pass
					else:
						if limit > 0 and not node.neighbors[n] in queue:
							limit = limit-1
							append_node = node.neighbors[n]
							queue.append(append_node)
							print("node: ("+ str(append_node.x) + "," + str(append_node.y)+") ")
							for q in queue:
								print("("+str(q.x) + ","+str(q.y)+")" + str(q.visited))
			print("##################################")

			print("============= current queue =========")
			print("queue size: "+ str(len(queue)))
			for queue_node in queue:
				if queue_node.visited:
					print(queue_node)
			print("===============end of current ========")
		
		print("after generate neighbors")
		print(len(visited_nodes))
		print(limit)
		print(i)
		'''

def v_sub(v1,v2):
	return (v1[0]-v2[0],v1[1]-v2[1])

def v_add(v1,v2):
	return (v1[0]+v2[0],v1[1]+v2[1])

def v_div(v1,s):
	return (v1[0]/s,v2[0]/s)

def generate_neighbors(center,dim,sensor):
	#calculate the center for each node
	center_up = v_add(center,(0,dim[1])) 		#0
	center_down = v_sub(center,(0,dim[1])) 		#1
	center_right = v_add(center,(dim[0],0))		#2
	center_left = v_sub(center,(dim[0],0))		#3
	center_q1 = v_add(center,dim)				#4
	center_q2 = v_add(center,(-dim[0],dim[1]))	#5
	center_q3 = v_sub(center,dim)				#6
	center_q4 = v_add(center,(dim[0],-dim[1]))	#7

	v_list = [center_up,center_down,center_right,center_left,
		center_q1,center_q2,center_q3,center_q4]
	node_list = []

	#generate all the neighbors
	for i in range(len(v_list)):
		c = v_list[i]
		if(sensor.check_within_boundary(V(c[0],c[1]))):
			node_list.append(c)
	return node_list


def connect_nodes(node_n):
	pass
	#post-assignment cleanup/hardcoding

	"""
				# q2up,upq2	# upup,q2q1 # upq1,q1up,#
				#			#	q1q2	#			#
	##########################################################
		q2l,lq2	# 	  q2	# 	up 		# q1 		# q1r,rq1
				#-----------#-----------#-----------#
	ll,q2q3,q3q2# 	left 	# 	node 	# right 	# rr,q1q4,q4q1
				#-----------#-----------#-----------#
		q3l,lq3	#	  q3 	#	down 	# q4 		# q4r,rq4
	###########################################################
				# q3d,dq3	#  dd,q3q4	#  q4d,dq4	#
				#			#	q4q3	#			#

				# 	9		# 	10		# 	11 		#
				#			#			#			#
	##########################################################
		20		# 	  1		# 	2 		# 	3 		# 12
				#-----------#-----------#-----------#
		19		# 	  8	 	# 	0	 	# 	4	 	# 13
				#-----------#-----------#-----------#
		18		#	  7 	#	6 	 	#   5 		# 14
	###########################################################
				# 	  17	#  	16		#  	15		#
				#			#			#			#
	"""

"""
	if node_n.neighbors["q1"] is not None:
		if node_n.neighbors["right"] is not None:
			node_n.neighbors["q1"].neighbors["down"] = node_n.neighbors["right"]
			node_n.neighbors["right"].neighbors["up"] = node_n.neighbors["q1"]
		if node_n.neighbors["up"] is not None:
			node_n.neighbors["q1"].neighbors["left"] = node_n.neighbors["up"]
			node_n.neighbors["up"].neighbors["right"] = node_n.neighbors["q1"]
	 
	if node_n.neighbors["q2"] is not None:
		if node_n.neighbors["left"] is not None:
			node_n.neighbors["q2"].neighbors["down"] = node_n.neighbors["left"]
			node_n.neighbors["left"].neighbors["up"] = node_n.neighbors["q2"]
		if node_n.neighbors["up"] is not None:
			node_n.neighbors["q2"].neighbors["right"] = node_n.neighbors["up"]
			node_n.neighbors["up"].neighbors["left"] = node_n.neighbors["q2"]
		q2 = node_n.neighbors["q2"]
		if q2.neighbors["up"] is not None:


	if node_n.neighbors["q3"] is not None:
		if node_n.neighbors["left"] is not None:
			node_n.neighbors["q3"].neighbors["up"] = node_n.neighbors["left"]
			node_n.neighbors["left"].neighbors["down"] = node_n.neighbors["q3"]
		if node_n.neighbors["down"] is not None:
			node_n.neighbors["q3"].neighbors["right"] = node_n.neighbors["down"]
			node_n.neighbors["down"].neighbors["left"] = node_n.neighbors["q3"]
	 
	if node_n.neighbors["q4"] is not None:
		if node_n.neighbors["right"] is not None:
			node_n.neighbors["q4"].neighbors["up"] = node_n.neighbors["right"]
			node_n.neighbors["right"].neighbors["down"] = node_n.neighbors["q4"]
		if node_n.neighbors["down"] is not None:
			node_n.neighbors["q4"].neighbors["left"] = node_n.neighbors["down"]
			node_n.neighbors["down"].neighbors["right"] = node_n.neighbors["q4"]

	if node_n.neighbors["up"] is not None:
		up = node_n.neighbors["up"]
		if node_n.neighbors["left"] is not None:
			node_n.neighbors["up"].neighbors["q3"] = node_n.neighbors["left"]
			node_n.neighbors["left"].neighbors["q1"] = node_n.neighbors["up"]
		if node_n.neighbors["right"] is not None:
			node_n.neighbors["up"].neighbors["q4"] = node_n.neighbors["right"]
			node_n.neighbors["right"].neighbors["q2"] = node_n.neighbors["up"]
		if node_n.neighbors["up"].neighbors["up"] is not None:
			if up.neighbors["left"] is not None:
				up.neighbors["up"].neighbors["q3"] = up.neighbors["left"]
				up.neighbors["left"].neighbors["q1"] = up.neighbors["up"]
			if up.neighbors["right"] is not None:
				up.neighbors["up"].neighbors["q4"] = up.neighbors["right"]
				up.neighbors["right"].neighbors["q2"] = up.neighbors["up"].neighbors["q4"]

	if node_n.neighbors["down"] is not None:
		down = node_n.neighbors["down"]
		if node_n.neighbors["left"] is not None:
			node_n.neighbors["down"].neighbors["q2"] = node_n.neighbors["left"]
			node_n.neighbors["left"].neighbors["q4"] = node_n.neighbors["down"]
		if node_n.neighbors["right"] is not None:
			node_n.neighbors["down"].neighbors["q1"] = node_n.neighbors["right"]
			node_n.neighbors["right"].neighbors["q3"] = node_n.neighbors["down"]
		if down.neighbors["down"] is not None:
			if down.neighbors["left"] is not None:
				down.neighbors["down"].neighbors["q2"] = down.neighbors["left"]
				down.neighbors["left"].neighbors["q4"] = down.neighbors["down"]
			if down.neighbors["right"] is not None:
				down.neighbors["down"].neighbors["q1"] = down.neighbors["right"]
				down.neighbors["right"].neighbors["q3"] = down.neighbors["down"]

	if node_n.neighbors["left"] is not None:
		left = node_n.neighbors["left"]
		if left.neighbors["left"] is not None:
			if left.neighbors["up"] is not None:
				left.neighbors["left"].neighbors["q1"] = left.neighbors["up"]
				left.neighbors["up"].neighbors["q3"] = left.neighbors["left"]
			if left.neighbors["down"] is not None:
				left.neighbors["left"].neighbors["q4"] = left.neighbors["down"]
				left.neighbors["down"].neighbors["q2"] = left.neighbors["left"]

	if node_n.neighbors["right"] is not None:
		right = node_n.neighbors["right"]
		if right.neighbors["right"] is not None:
			if right.neighbors["up"] is not None:
				right.neighbors["right"].neighbors["q2"] = right.neighbors["up"]
				right.neighbors["up"].neighbors["q4"] = right.neighbors["right"]
			if right.neighbors["down"] is not None:
				right.neighbors["right"].neighbors["q3"] = right.neighbors["down"]
				right.neighbors["down"].neighbors["q1"] = right.neighbors["right"]	
"""



"""
def generate_neighbors(node_n,sensor):
	center = (node_n.x,node_n.y)
	dim = node_n.get_dim()
	#calculate the center for each node
	center_up = v_add(center,(0,dim[1])) 		#0
	center_down = v_sub(center,(0,dim[1])) 		#1
	center_right = v_add(center,(dim[0],0))		#2
	center_left = v_sub(center,(dim[0],0))		#3
	center_q1 = v_add(center,dim)				#4
	center_q2 = v_add(center,(-dim[0],dim[1]))	#5
	center_q3 = v_sub(center,dim)				#6
	center_q4 = v_add(center,(dim[0],-dim[1]))	#7

	v_list = [center_up,center_down,center_right,center_left,
		center_q1,center_q2,center_q3,center_q4]
	node_list = []

	#generate all the neighbors
	for i in range(len(v_list)):
		c = v_list[i]
		if(sensor.check_within_boundary(V(c[0],c[1]))):
			node_list.append(Node(c[0],c[1]))
		else:
			node_list.append(None)
	
	#node position wrt list position	
	key_dict = dict(up=0,down=1,right=2,left=3,q1=4,q2=5,q3=6,q4=7)
	#current node assignment to new neighbor
	modify_vs_node = dict(up="down",down="up",right="left",left="right",q1="q3",q2="q4",q3="q1",q4="q2")
	
	new = 0
	#assign neighbor to this node
	for n in node_n.neighbors.keys():
		if node_n.neighbors[n] == None and node_list[key_dict[n]] is not None:
			new = new + 1
			modify_node = node_list[key_dict[n]]
			#assign shape and node_n role to the new neighbor
			modify_node.set_shape(node_n.shape)
			modify_node.neighbors[modify_vs_node[n]] = node_n
			#actual assignment
			node_n.neighbors[n] = modify_node

	print("discovered " + str(new) + " nodes")
	connect_nodes(node_n)

"""



def check_within_rectangle(rectangle,vertex):
	pass




#sensing checking surroundings for robot
class Sensor():
	def __init__(self,owner,obstcles,dim):
		self.owner = owner
		self.obs = obstcles
		self.space_dim = dim
	#return if shape collide with obstacles
	def check_with_obs(self,shape):
	    for actor in obstacle:
	        for p in actor.get_parts():
	            overlap,direction=check_xy_overlap(shape,p)
	            if(overlap):
	                return overlap
	    return False
	def check_point_with_obs(self,v):
		point = Shape("point",v)

	def check_within_boundary(self,v):
		return v.x>0 and v.x <self.space_dim[0] and v.y>0 and v.y < self.space_dim[1]