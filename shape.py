import numpy
from vertex import V
from math import pi,sin,cos

"""
Shape class:
	stores basic information regarding 2D shapes
"""
class Shape(object):
	
	def __init__(self,type,v):
		#guard against lack of sleep
		if(len(v) == 0):
			raise ValueError("Empty Input")
		
		self.type = type 	#circle or polygon
		self.v = v 			#list of vertices
		#TODO: self.center = self.compute_center()

	#print function
	def __repr__(self):
		s = ""
		for vertex in self.v:
			s += str(vertex)
		return "type: " + self.type + " v: " + s

	#get type
	def get_type(self):
		return self.type

	#get list of vertices
	def get_vertices(self):
		return self.v

	#rotation
	#TODO: def rotate(self,angle)

	#linear transformation
	def translate(self,vector):
		for vertex in self.v:
			vertex.move(vector)

	#get position
	def get_pos(self):
		flat_list = []
		for vertex in self.v:
			t = vertex.get_pos()
			flat_list.extend(list(t))
		return tuple(flat_list)

#=============================================================


"""
class Circle(Shape):
	def __init__(self,c,r):

		if(r <= 0):
			raise ValueError("Invalid radius")

		Shape.__init__(self,"circle",[c]) #send center of circle in
		self.radius = r

	#print statement
	def __repr__(self):
		s = Shape.__repr__(self)
		s += " rardius: "+ str(self.radius)
		return  s

	#retrieve radius
	def get_radius(self):
		return self.radius

	#return list of vertices at the circumference
	#it's an approximation of a circle
	def get_pos(self):
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

	#TODO: how do I represent circle in quadtree?
"""
class Polygon(Shape):
	def __init__(self,v):
		Shape.__init__(self,"polygon",v)








if __name__ == '__main__':
	v1 = V(0,0)
	v2 = V(0,2)
	v3 = V(2,0)
	shape1 = Shape("polygon",[v1,v2,v3])
	print(shape1)
	print("translate by 1,1")
	shape1.translate([1,1])
	print(shape1)
	print(shape1.get_pos())
	print("========end of testing shape======")

	#c1 = Circle(V(1,1),1.5)
	#print(c1)
	#print(c1.get_pos())

	print("========end of testing circle=======")

	p1 = Polygon([V(0,0),V(1,0),V(1,1),V(0,1)])
	print(p1)