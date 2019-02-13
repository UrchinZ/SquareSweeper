import pyglet, math
from pyglet.window import key
from actor import Actor

class Robot(Actor):
	def __init__(self, *args, **kwargs):
		#super(Robot,self).__init__(*args, **kwargs)
		self.fix = False
		self.key_handler = key.KeyStateHandler()
		self.event_handlers = [self, self.key_handler]

	def on_key_press(self, symbol, modifiers):
		if symbol == key.SPACE:
			print("space presed")