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
		print("I need to do some dijkstra stuff")
		if not self.map:
			self.construct_belief_map()

		if (len(self.dest) == 0):
			print("exiting dijkstra function")
			return
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
		print("my center is: " + str(my_center))
		i = Node(my_center.x,my_center.y)
		print(i)
		#bfs queue
		queue = [i]
		











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