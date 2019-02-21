import pyglet
from pyglet.window import key
from actor import Actor
from shape import *

#specialized actor robot
class SquareRobot(Actor):
	def __init__(self):
		DIM = (100,100)
		center = (50,50)
		v1 = V(center[0]-DIM[0]/2, center[1]-DIM[1]/2)
		#v2 = V(center[0]-DIM[0]/2, center[1]+DIM[1]/2)
		#v3 = V(center[0]+DIM[0]/2, center[1]+DIM[1]/2)
		#v4 = V(center[0]+DIM[0]/2, center[1]-DIM[1]/2)
		#self.parts = [Polygon([v1,v2,v3,v4])]
		self.parts = [Rectangle(v1,width = DIM[0],height=DIM[1])]
		self.actor_type = "robot"
		#self.key_handler = key.KeyStateHandler()
		#self.event_handlers = [self, self.key_handler]
		self.speed = 5
		self.keys = dict(left=False, right=False, up=False, down=False)

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


	def update(self,dt,DIM):
		#print("update in robot " + str(dt))
		if self.keys['up']:
			self.move((0,1*self.speed),DIM)
		if self.keys['down']:
			self.move((0,-1*self.speed),DIM)
		if self.keys['left']:
			self.move((-1*self.speed,0),DIM)
		if self.keys['right']:
			self.move((1*self.speed,0),DIM)



