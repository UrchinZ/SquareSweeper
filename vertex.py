"""
Vertex class:
	contain information regarding one vertex
"""
class V:
	def __init__(self, x, y):
		self.x  = x
		self.y = y
	
	#return vertex position in a tuple
	def get_pos(self):
		return (self.x, self.y)

	#set current posiiton to new value
	def set_pos(self,second,third = None):
		print("set new value" + str(second))
		if third is None:
			self.x = second[0]
			self.y = second[1]
		else:
			self.x = second
			self.y = third

	#move vertex based on position
	def move(self,vector):
		print("move vertex")
		value = (self.x + vector[0], self.y + vector[1])
		self.set_pos(value)

	#print vertex information
	def __repr__(self):
		return str(self.get_pos())


if __name__ == '__main__':
	print("testing basic functions:")
	v = V(1,1)
	print(v)
	v.set_pos((2,2))
	print(v)
	v.set_pos(1,3)
	print(v)
	v.move((-1,-1))
	print(v)
	print("========================")