"""
simulator = stage
"""
from actor import *
from render import *
import sys

class Simulator():
	def __init__(self,window,dt):
		self.window = window
		self.mov = []
		self.obs = []
		self.dirt = []
		self.dt = dt
	
	def add_actor(self,actor):
		if not actor.movable:
			self.obs.append(actor)
		elif actor.dust:
			self.dirt.append(actor)
		else:
			self.mov.append(actor)
	
	def add_actors(self,actors):
		for actor in actors:
			self.add_actor(actor)

	def get_actors(self):
		actors = mov + obs + dirt
	

def main():
	c = Circle(V(1,1),100)
	p = Polygon([V(300,400),V(200,200),V(200,300)])
	oo = Object(False,True,2,[c,p])
	print("first object")
	print(oo)

	r = Polygon([V(0,0),V(100,0),V(100,100),V(0,100)])
	robot = Object(True,False,1,[r])
	print("second object")
	print(robot)

	window = ShapeWindow(width=400, height=400)
	sim = Simulator(window,0.1)
	sim.add_actors([oo,robot])
	pyglet.app.run()
main()