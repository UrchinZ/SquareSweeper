import pyglet
import actor
from robot import Robot

class Simulator(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        DIM = (700,500) #window dimensions
        super(Simulator,self).__init__(width=DIM[0],
        height = DIM[1], *args, **kwargs)
        window = self
        pyglet.gl.glClearColor(0.10, 0.10, 0.0,0.0)
        window.clear()

        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
        [0, 1, 2, 0, 2, 3],
        ('v2i', (100, 100,
                 150, 100,
                 150, 150,
                 100, 150))
        )

        #get robot
        square_robot = Robot()

        for eh in square_robot.event_handlers:
            window.push_handlers(eh)


