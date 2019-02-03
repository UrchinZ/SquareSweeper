"""
file containing all the geomtry displayed
"""

"""
Vertex position
"""
class V:
	def __init__(self, x, y):
		self.x  = x
		self.y = y

	def add(self, vec):
		self.x += vec.x
		self.y += vec.y

	def sub(self, vec):
		self.x -= vec.x
		self.y -= vec.y

	def mult(self, scalar):
		self.x *= scalar
		self.y *= scalar

	def mag(self):
		return sqrt(self.x ** 2 + self.y ** 2)

	def copy(self):
		return Vec2(self.x, self.y)

	def coords(self):
		return (self.x, self.y)

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


"""
circle
"""
class Circle(Shape):
	def __init__(self,c,r):
		if(r <= 0):
			raise ValueError("Invalid radius")
		Shape.__init__(self,"circle",[c])
		self.radius = r

	def __repr__(self):
		s = Shape.__repr__(self)
		s += " rardius: "+ str(self.radius)
		return  s
"""
polygon
"""
class Polygon(Shape):
	def __init__(self,v):
		Shape.__init__(self,"polygon",v)

"""
Object properties:
1. how many pieces does it contain
2. can we move it?
3. how tall is it? (if lower than the robot, we can suck it in)
"""
class Object():
	def __init__(self, part, movable, height):
		self.part = part
		self.movable = movable
		self.height = height

	def __repr__(self):
		s = "part: "+str(self.part) + " movable: "
		s += str(self.movable) + " height: "+ str(self.height)
		return s 


def main():
	o = Object(1,True,0.01)
	print(o)
	c = Circle(V(1,1),1)
	print(c)
	p = Polygon([V(1,1),V(2,2),V(1,3)])
	print(p)


if __name__ == '__main__':
	main()