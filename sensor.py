from actor import Actor
from shape import *
from graph import *
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry.polygon import Polygon as ShapelyPolygon
from shapely.geometry import LineString
import random
import math

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

	#return a point that is not in obstacle
	def get_rand_free(self):
		point = self.get_rand_in_cspace(1)
		while self.collide_with_obs(point[0]):
			point = self.get_rand_in_cspace(1)
		return point[0]

	def get_rand_in_cspace(self, n):
		space = self.space_dim
		robot_dim = self.owner.get_dim()
		#cspace = (robot_dim[0], space[0]-robot_dim[0], robot_dim[1], space[1]-robot_dim[1])
		cspacex = (robot_dim[0]/2, space[0]-robot_dim[0]/2)
		cspacey = (robot_dim[1]/2, space[1]-robot_dim[1]/2)
		x_dist = cspacex[1] - cspacex[0]
		y_dist = cspacey[1] - cspacey[0]

		print(str(cspacex) + " cspacex | "+str(cspacey)+ " cspacey")

		rand_points = []
		for pt in range(n):
			x = random.randrange(*(cspacex))
			y = random.randrange(*(cspacey))
			rand_points.append((x,y))
		return rand_points


	def extend(self,start,end):
		#speed = self.owner.speed
		speed = int(self.owner.get_dim()[0]/2)
		print("robot speed: " + str(speed))
		
		total_length = length(start,end)
		print("robot total length: " + str(total_length))

		path_list = []
		steps = int(math.floor(total_length/speed))
		
		if steps == 0:
			path_list.append(start)

		for s in range(steps):
			size = s * speed/total_length
			print("size: " + str(size))
			point = (int(math.floor(size*end[0] + (1-size)*start[0])), 
				int(math.floor(size*end[1] + (1-size)*start[1])))
			print("new point: " + str(point))
			path_list.append(point)
		path_list.append(end)
		return path_list


	def check_in_cfree(self,pos):
		space = self.space_dim
		robot_dim = self.owner.get_dim()
		cspacex = (robot_dim[0]/2, space[0]-robot_dim[0]/2)
		cspacey = (robot_dim[1]/2, space[1]-robot_dim[1]/2)
		if(pos[0]<cspacex[0] or pos[0] >cspacex[1] or pos[1]<cspacey[0] or pos[1]>cspacey[1]):
			return False
		if self.collide_with_obs(pos):
			return False
		return True



	#check collision and return the closest point robot can reach
	def check_path(self, start, end):
		"""
		print("inside check path: " + str(start) + " to " + str(end))
		dim = self.owner.get_dim()
		#half the dimension
		hdx = dim[0]/2
		hdy = dim[1]/2
		
		#locate points
		lower = start
		top = end
		
		if (start[1] > end[1]):
			lower = end
			upper = start
		
		left = start
		right = end
		
		if(start[0] > end[0]):
			left = end
			right = start

		#calculate points
		lower_x_min = (lower[0]-hdx, lower[1]-hdy)
		lower_x_max = (lower[0] + hdx, lower[1]-hdy)
		right_y_min = (right[0] + hdx, right[1]-hdy)
		right_y_max = (right[0] + hdx, right[1]+hdy)
		top_x_max = (top[0] + hdx, top[1] + hdy)
		top_x_min = (top[0] - hdx, top[1] + hdy)
		left_y_max = (left[0] - hdx, left[1] + hdy)
		left_y_min = (left[0] - hdx, left[1] - hdy)

		path = ShapelyPolygon([lower_x_min, lower_x_max,right_y_min,right_y_max,top_x_max,top_x_min,left_y_max,left_y_min])
		print("robot path exterior: ")
		print(list(path.exterior.coords))
		#test = [(25,25), (50,70), (32, 49), (120, 120), (60,5), (0, 78)]

		#for t in test:
		#	print("test point " + str(t))
		#	point = ShapelyPoint(t)
		#	print(path.contains(point))
		print("checking points")
		o = []
		for obstacle in self.obs:
			parts = obstacle.get_parts();
			for part in parts:
				verticles = part.get_pos()
				points = []
				for i in range(0,len(verticles),2):
					points.append((verticles[i],verticles[i+1]))
				print(points)
				for p in points:
					point = ShapelyPoint(p)
					if path.contains(point):
						print("contains")
						o.append(part)
		print("there are: "+str(len(o)) + " obstacles within path")
		print(o)

		for obs in o:
			assert(len(obs.get_pos()) == 8)
			center = obs.get_center()
			DIM = self.owner.get_dim()
			width = obs.get_width() + DIM[0]
			height = obs.get_height() + DIM[1]
			x_min = center.x-width/2
			x_max = center.x+width/2
			y_min = center.y-height/2
		"""
		print("inside check path: " + str(start) + " to " + str(end))
		dim = self.owner.get_dim()
		robot_path = LineString([start,end])


		obs_shapes = []
		for obs in self.obs:
			parts = obs.get_parts();
			obs_shapes.extend(parts)
		print(len(obs_shapes))
		print(obs_shapes)
		oshape = []
		intersection = []
		print("obstacle space:")
		for obs in obs_shapes:
			center = obs.get_center()
			width = obs.get_width() + dim[0]
			height = obs.get_height() + dim[1]
			x_min = center.x-width/2
			x_max = center.x+width/2
			y_min = center.y-height/2
			y_max = center.y+height/2
			path = ShapelyPolygon([(x_min,y_min), (x_max,y_min),(x_max,y_max),(x_min,y_max)])
			oshape.append(path)
			print(list(path.exterior.coords)) #debug statement
			i = path.intersection(robot_path)
			if(not i.is_empty):
				intersection.append(i)

		print("all intersections: ")
		print(intersection)
		# all points
		interest = []
		for p in intersection:
			interest.extend(list(p.coords))
		print interest
		print("sorted")
		sorted(interest, key=lambda x: (x[0]-start[0])**2 + (x[1]-start[1])**2)
		print interest	
		if(len(interest) > 0):
			closest_point = interest[0]
			return (int(math.floor(closest_point[0])),int(math.floor(closest_point[1])))
		else:
			return None	



		
