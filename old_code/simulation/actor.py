import pyglet


class Actor():
	def __init__(self, *args, **kwargs):
		#super(Actor,self).__init__(*args, **kwargs)

		#flags for obstacles
		self.fixed = True
		# Tell the game handler about any event handlers
		# Only applies to things with keyboard/mouse input
		self.event_handlers = []

"""
	def show():
		pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
		    ('v2f', (0,0,0,100,100,100,100,0 ))
		)
"""