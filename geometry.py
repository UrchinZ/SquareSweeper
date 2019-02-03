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
2D geomtry circle
"""
class Circle:
	def __init__(self,c,r):
		if(r <= 0):
			raise ValueError("Invalid radius")
		self.type="circle"
		self.pos = c
		self.radius = r

	def __repr__(self):
		s = "type: "+self.type + " pos: "+str(self.pos)
		s += " rardius: "+ str(self.radius)
		return  s
"""
2D polygon
"""
class Polygon:
	def __init__(self,v):
		length = len(v)
		if length == 0:
			raise NameError("empty input")

		self.type = "polygon"
		self.num = len(v)
		self.v = v
	
	def __repr__(self):
		return self.type + " num: "+self.num + "\nv: " + str(self.v) 

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


if __name__ == '__main__':
	main()