import pyglet, time
from pyglet.window import mouse
from pyglet.window import key
from actor import Actor
from shape import *
from graph import *

#specialized actor robot
class SquareRobot(Actor):
	def __init__(self):
		#start with left bottom corner
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
		self.keys = dict(left=False, right=False, up=False, down=False, 
					dijk = False, a_star = False)
		self.dest = []
		self.map = None
		self.path = []
	
	def get_center(self):
		center_v = self.parts[0].get_center()
		return (center_v.x,center_v.y)

	def get_center_v(self):
		return self.parts[0].get_center()

	def get_dim(self):
		return (self.parts[0].get_width(),self.parts[0].get_height())

	def set_sensor(self,sensor):
		self.sensor = sensor
		self.construct_belief_map()
		print("done with setup")

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
			print("Running Dijk's...")
			self.keys["dijk"] = True
		elif symbol == key.A:
			print("Running A*...")
			self.keys["a_star"] = True


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
	
	#change actors to sensor
	def update(self,dt,DIM,actors):
		#print("update in robot " + str(dt))
		if len(self.path) == 0:
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
			if self.keys['a_star']:
				self.a_star()
		else:
			self.path_update(dt,DIM,actors)
	
	def path_update(self,dt,DIM,actors):
		if len(self.path) == 0:
			return
		print("path_update to")
		goal = self.path[0]
		print(goal)
		current = self.get_center()
		if goal == current:
			self.path.pop(0)
			return
		difference = v_sub(goal,current)
		sign = [0,0]
		if difference[0] != 0:
			sign[0] = difference[0]/abs(difference[0])
		if difference[1] != 0:
		 	sign[1] = difference[1]/abs(difference[1])
		move = list(difference)
		if abs(difference[0]) >= self.speed:
			move[0] = sign[0]*self.speed
		if abs(difference[1]) >= self.speed:
			move[1] = sign[1]*self.speed
		self.move(move,DIM,actors)




	def dijk(self):
		if (len(self.dest) == 0):
			print("exiting dijkstra function")
			return

		if (self.sensor == None):
			print("do not have sensor")
			return

		print("I need to do some dijkstra stuff")
		
		print("running to destination:")
		destination = self.dest.pop(0)
		print(destination)
		dest = self.map.locate_node(destination)
		print(dest)
		self.map.set_dest(dest)
		print("from:")
		start_position = self.parts[0].get_center()
		print(start_position)
		start = self.map.locate_node(start_position)
		print(start)
		self.map.set_start(start)

		path = self.map.dijkstras()
		print("path generated:")
		print(path)
		self.path = path
			

		self.keys['dijk'] = False
		print("done with dijkstra")


	def a_star(self):
		if (len(self.dest) == 0):
			print("No exiting a_star function")
			return

		if (self.sensor == None):
			print("do not have sensor")
			return

		#locate destination
		destination = self.dest.pop(0)
		print("a_star: running to desination" + str(destination))
		dest = self.map.locate_node(destination)
		print("a_star: inside node: " + str(dest))

		#locate start
		start_position = self.get_center_v()
		start = self.map.locate_node(start_position)
		print("a_star: from: "+str(start_position) + 
			" inside node entered: "+ str(start))

		#run a_star magic
		self.map.set_dest(dest)
		self.map.set_start(start)
		path = self.map.a_star()
		print("a_star: path: " + str(path))

		#set robot path to planned path
		self.path = path
		
		self.keys["a_star"] = False
		print("done with a_star")



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
				if (neighbor not in queue) and (
					neighbor not in visited_nodes.keys()):
					queue.append(neighbor)
			#mark position in visited node
			visited_nodes[pos] = None
		#print("inside construction queue: ")
		#print("visited_nodes:")
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
				"""
				elif index == 4:
					node.assign_neighbor("q1",neighbor_node)
				elif index == 5:	
					node.assign_neighbor("q2",neighbor_node)
				elif index == 6:
					node.assign_neighbor("q3",neighbor_node)
				elif index == 7:
					node.assign_neighbor("q4",neighbor_node)
				"""
		print("post stitching:")
		print(visited_nodes)
		for pos,node in visited_nodes.items():
			node.set_shape(Rectangle(V(pos[0]-dim[0]/2,pos[1]-dim[1]/2),width = dim[0],height=dim[1]))
		graph = Graph()
		graph.set_graph(visited_nodes)
		self.map = graph



def possible_neighbors(center,dim):
	#calculate the center for each node
	center_up = v_add(center,(0,dim[1])) 		#0
	center_down = v_sub(center,(0,dim[1])) 		#1
	center_right = v_add(center,(dim[0],0))		#2
	center_left = v_sub(center,(dim[0],0))		#3
	#center_q1 = v_add(center,dim)				#4
	#center_q2 = v_add(center,(-dim[0],dim[1]))	#5
	#center_q3 = v_sub(center,dim)				#6
	#center_q4 = v_add(center,(dim[0],-dim[1]))	#7

	v_list = [center_up,center_down,center_right,center_left]
		#center_q1,center_q2,center_q3,center_q4]
	return v_list


def v_sub(v1,v2):
	return (v1[0]-v2[0],v1[1]-v2[1])

def v_add(v1,v2):
	return (v1[0]+v2[0],v1[1]+v2[1])

def v_div(v1,s):
	assert(s != 0)
	return (v1[0]/s,v2[0]/s)

def v_time(v1,s):
	return (v1[0]*s,v2[0]*s)



def generate_neighbors(center,dim,sensor):
	v_list = possible_neighbors(center,dim)
	node_list = []

	#generate all the neighbors
	for i in range(len(v_list)):
		c = v_list[i]
		#TODO add check with collision
		if(sensor.check_within_boundary(V(c[0],c[1])) and not sensor.collide_with_obs(c)):
			node_list.append(c)
	return node_list




#sensing checking surroundings for robot
class Sensor():
	def __init__(self,owner,obstcles,dim):
		self.owner = owner
		self.obs = obstcles
		self.space_dim = dim
		self.virtual_pos = owner.get_center()

	def collide_with_obs(self,pos):
		print("check with obstacle")
		self.virtual_pos = V(pos[0],pos[1])
		for obstacle in self.obs:
			parts = obstacle.get_parts()
			for p in parts:
				if self.check_with_obs(p):
					print("would collide with obstacle part")
					print(p)
					print(self.virtual_pos)
					return True
		return False

	#return if shape collide with obstacles
	def check_with_obs(self,shape):
		DIM = self.owner.get_dim()
		v1 = V(self.virtual_pos.x-DIM[0]/2, self.virtual_pos.y-DIM[1]/2)
		p = Rectangle(v1,width = DIM[0],height=DIM[1])
		print("virtual position")
		print(p)
		overlap,direction=check_xy_overlap(shape,p)
		return overlap
	
	def check_within_boundary(self,v):
		return v.x>0 and v.x <self.space_dim[0] and v.y>0 and v.y < self.space_dim[1]