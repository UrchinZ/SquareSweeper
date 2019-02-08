#!/usr/bin/env python

import yaml
import pyglet
from math import pi,sin,cos
"""
file containing all the geomtry displayed
"""
#https://www.programsinformationpeople.org/runestone/static/publicpy3/Pyglet/windowContents.html
"""
Vertex position
"""
class V:
	def __init__(self, x, y):
		self.x  = x
		self.y = y

	def coords(self):
		return (self.x, self.y)

	def move(self,vec):
		self.x += vec[0]
		self.y += vec[1]

	def up(self,scalar):
		self.y += scalar

	def down(self,scalar):
		self.y -= scalar

	def left(self,scalar):
		self.x -= scalar

	def right(self,scalar):
		self.x += scalar

	def __repr__(self):
		return str(self.coords())

"""
2D shapes
"""
class Shape(object):
	def __init__(self,type,v):
		if(len(v) == 0):
			raise ValueError("Empty Input")
		self.type = type
		self.v = v
	def __repr__(self):
		s = ""
		for vertex in self.v:
			s += str(vertex)
		return "type: " + self.type + " v: " + s

	#get position
	def get_v(self):
		return self.v

	def get_type(self):
		return self.type

	#move in specific four directions
	def move_direction(self,direction,scalar):
		for vertex in self.v:
			if direction == "up":
				vertex.up(scalar)
			elif direction == "down":
				vertex.down(scalar)
			elif direction == "left":
				vertex.left(scalar)
			elif direction == "right":
				vertex.right(scalar)
	
	#move by vector
	def move(self,vec):
		for vertex in self.v:
			v.move(vec)
	
"""
circle
"""
class Circle(Shape):
	def __init__(self,c,r):
		if(r <= 0):
			raise ValueError("Invalid radius")
		Shape.__init__(self,"circle",[c])
		self.radius = r

	def get_radius(self):
		return self.radius

	def __repr__(self):
		s = Shape.__repr__(self)
		s += " rardius: "+ str(self.radius)
		return  s

	#return list of vertices at the circumference
	#it's an approximation of a circle
	def show(self):
		pos = self.v[0]
		p = int(self.radius*2)
		angle = 0
		increment = (pi * 2) / p
		coords = []
		for i in range(0, p):
			x = self.radius * sin(angle) + pos.x
			y = self.radius * cos(angle) + pos.y
			coords.append(x)
			coords.append(y)
			angle += increment
		return tuple(coords)

"""
polygon
"""
class Polygon(Shape):
	def __init__(self,v):
		Shape.__init__(self,"polygon",v)

	#return list of vertices to draw
	def show(self):
		flat_list = []
		for l in self.v:
			t = l.coords()
			flat_list.extend(list(t))
		return tuple(flat_list)



"""
Object properties:
1. how many pieces does it contain
2. can we move it? (is it heavy enough to move)
3. can we suck it in?/ Is it dust?
"""
class Object(object):
	def __init__(self, movable, dust, piece_num,pieces):
		self.movable = movable
		self.dust = dust
		self.num = piece_num
		self.pieces = pieces

	def get_pieces(self):
		return self.pieces

	def up(self,value):
		for piece in self.pieces:
			piece.move_direction("up",value)

	def down(self,value):
		for piece in self.pieces:
			piece.move_direction("down",value)

	def left(self,value):
		for piece in self.pieces:
			piece.move_direction("left",value)

	def right(self,value):
		for piece in self.pieces:
			piece.move_direction("right",value)


	def __repr__(self):
		s = "movable: "+str(self.movable) + " dust "+ str(self.dust)
		s += " piece num: "+str(self.num) + "\n"
		for shape in self.pieces:
			s += str(shape)+'\n'
		return s 

#some testing
def main():
	c = Circle(V(1,1),200)
	print(c)
	#print(c.show())
	p = Polygon([V(1,1),V(2,2),V(1,3)])
	print(p)
	print(len(p.show()))
	print("first object")
	o = Object(True,True,1,[c])
	print(o)
	print("second object:")
	oo = Object(True,True,2,[c,p])
	print(oo)

	with open("./config/test.yaml", 'r') as stream:
	    info = yaml.load(stream)
	    print(info)
	pyglet.app.run()


if __name__ == '__main__':
	game_window = pyglet.window.Window()
	game_window.clear()
	main()