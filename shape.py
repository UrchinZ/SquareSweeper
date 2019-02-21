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


"""
Rectangle class
"""
class Rectangle(Polygon):
	def __init__(self,*args, **kwargs):
		self.width = 0;
		self.height = 0;
		if(len(args)==4):
			Polygon.__init__(self,list(args))
			v1,v2,v3,v4 = args
			x1,y1 = (v1.x,v1.y)
			x2,y2 = (v2.x,v2.y)
			x3,y3 = (v3.x,v3.y)
			x4,y4 = (v4.x,v4.y)
			self.width = max(x1,x2,x3,x4) - min(x1,x2,x3,x4)
			self.height = max(y1,y2,y3,y4) - min(y1,y2,y3,y4)
		else:
			self.width = kwargs.get('width',0)
			self.height = kwargs.get('height',0)
			lbcV = args[0]
			lucV = V(lbcV.x, lbcV.y + self.height)
			rbcV = V(lbcV.x + self.width, lbcV.y)
			rucV = V(lbcV.x + self.width, lbcV.y + self.height)
			Polygon.__init__(self,[lbcV,rbcV,rucV,lucV])
		#self.type = "rectangle"
	
	def get_width(self):
		return self.width
	def get_height(self):
		return self.height

'''
function checks if bounding box of x and y direction overlap
'''
def check_xy_overlap(s1,s2):
	vertices1 = s1.get_vertices()
	vertices2 = s2.get_vertices()
	x_max_1,x_max_2,y_max_1,y_max_2 = 0,0,0,0
	x_min_1,y_min_1,x_min_2,y_min_2 = float('inf'),float('inf'),float('inf'),float('inf')

	for v in vertices1:
		x_max_1 = max(x_max_1,v.x)
		x_min_1 = min(x_min_1,v.x)
		y_max_1 = max(y_max_1,v.y)
		y_min_1 = min(y_min_1,v.y)
	
	for v in vertices2:
		x_max_2 = max(x_max_2,v.x)
		x_min_2 = min(x_min_2,v.x)
		y_max_2 = max(y_max_2,v.y)
		y_min_2 = min(y_min_2,v.y)
	#checks for x direction
	x_dir = ((x_min_1 <= x_min_2 and x_min_2 < x_max_1) or 
		(x_min_1 < x_max_2 and x_max_2 <= x_max_1))

	y_dir = ((y_min_1 <= y_min_2 and y_min_2 < y_max_1) or 
		(y_min_1 < y_max_2 and y_max_2 <= y_max_1))

	print(x_dir)
	print(y_dir)
	return x_dir and y_dir



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

	print("test rectangle")
	r1 = Rectangle(V(0,0),V(1,0),V(1,1),V(0,1))
	r2 = Rectangle(V(3,0), width=1,height=2)
	print(r1.get_height())
	print(r2.get_width())
	print(r2)
	print(check_xy_overlap(r1,r2))