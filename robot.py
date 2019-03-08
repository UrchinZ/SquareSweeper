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

	def on_mouse_press(self, x, y, button, modifiers):
		if button == 1:
			#pyglet doesn't respond to clicks outside the stage
			self.dest.append(V(x,y))
			#I might want to sort dest
			print(self.dest)
	
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

		
		print("running to destinations:")
		print(self.dest)
		self.locate_dest()


		while len(self.dest):
			time.sleep(2)
			destination = self.dest.pop(0)

		self.keys['dijk'] = False


	def locate_dest(self):
		for d in self.dest:
			for key,node in self.map.items():
				inside,loc = p_inside_rect(d,node.shape)
				if inside == True:
					print("inside: "+str(key))




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
		print("inside construction queue: ")
		print(queue)
		print(len(queue))
		print("visited_nodes:")
		print(visited_nodes)
		print(len(visited_nodes.keys()))
		
		#construct node for all positions
		for key,value in visited_nodes.items():
			if(value == None):
				visited_nodes[key] = Node(key[0],key[1])

		#stitch nodes up
		for pos,node in visited_nodes.items():
			neighbor_list = possible_neighbors(pos,dim)
			#print("neighbor list for "+str(pos))
			#print(neighbor_list)
			for index in range(len(neighbor_list)):
				neighbor = neighbor_list[index]
				#skip if not in visited node
				if neighbor not in visited_nodes.keys():
					continue
				neighbor_node = visited_nodes[neighbor]
				"""
				#####################################
				# 	  q2 5	# 	up 	0	# q1 	4	# 
				#-----------#-----------#-----------#
				# 	left 3	# 	node 	# right 2	# 
				#-----------#-----------#-----------#
				#	  q3 6	#	down 1	# q4 	7	#
				#####################################
				"""
				#assign relative position based on index
				if index == 0:
					node.assign_neighbor("up",neighbor_node)
				elif index == 1:
					node.assign_neighbor("down",neighbor_node)
				elif index == 2:
					node.assign_neighbor("right",neighbor_node)
				elif index == 3:
					node.assign_neighbor("left",neighbor_node)
				elif index == 4:
					node.assign_neighbor("q1",neighbor_node)
				elif index == 5:	
					node.assign_neighbor("q2",neighbor_node)
				elif index == 6:
					node.assign_neighbor("q3",neighbor_node)
				elif index == 7:
					node.assign_neighbor("q4",neighbor_node)
		print("post stitching:")
		print(visited_nodes)
		for pos,node in visited_nodes.items():
			node.set_shape(Rectangle(V(pos[0],pos[1]),width = dim[0],height=dim[1]))
		self.map = visited_nodes



def possible_neighbors(center,dim):
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
	return v_list


def v_sub(v1,v2):
	return (v1[0]-v2[0],v1[1]-v2[1])

def v_add(v1,v2):
	return (v1[0]+v2[0],v1[1]+v2[1])

def v_div(v1,s):
	return (v1[0]/s,v2[0]/s)



def generate_neighbors(center,dim,sensor):
	v_list = possible_neighbors(center,dim)
	node_list = []

	#generate all the neighbors
	for i in range(len(v_list)):
		c = v_list[i]
		if(sensor.check_within_boundary(V(c[0],c[1]))):
			node_list.append(c)
	return node_list




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