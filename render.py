import pyglet
import sys
from math import *
from actor import *

class ShapeWindow(pyglet.window.Window):

    #args pass in non-keyworded variable length argument list
    # use: for arg in argv:
    #kwargs pass keyworded variable length of arguments
    # use: for key, value in kwargs.iteritems()
    #https://pythontips.com/2013/08/04/args-and-kwargs-in-python-explained/
    def __init__(self,*args,**kwargs):
        pyglet.window.Window.__init__(self)
        #set color
        pyglet.gl.glClearColor(0.10, 0.10, 0.0,0.0)
        #clear window
        self.clear()
        # The game loop
        pyglet.clock.schedule_interval(self.update, 1 / 60)
        #track a list of actors
        self.actors = []

    def add_actor(self, act):
        self.actors.append(act)

    def on_draw(self):
        print('Draw simulation')
        sys.stdout.flush()
        for a in self.actors:
            for shape in a.get_pieces():
                v = shape.show()
                if(shape.get_type() == "circle"):
                    self.draw_circle(v)
                else: #for now definitely polygon
                    self.draw_polygon(v)

    #allow keyboard control
    def on_key_press(self,key,modifiers):
        if key == pyglet.window.key.UP:
            print("up")
        elif key == pyglet.window.key.DOWN:
            print("down")
        elif key == pyglet.window.key.RIGHT:
            print("right")
        elif key == pyglet.window.key.LEFT:
            print("left")

    #OpenGL syntax for drawing filled circle
    def draw_circle(self,v):
        num = len(v)/2
        pyglet.graphics.draw(num, 
            pyglet.gl.GL_TRIANGLE_FAN,("v2f", v))

    #OpenGL syntax for drawing polygon
    def draw_polygon(self,v):
        num = len(v)/2
        pyglet.graphics.draw(num, pyglet.gl.GL_POLYGON,
        ('v2i',v))

    def update(self, dt):
        pass


if __name__ == '__main__':
    shape_window = ShapeWindow()
    c = Circle(V(1,1),100)
    print(c)
    p = Polygon([V(300,400),V(200,200),V(200,300)])
    print(p)
    print("first object")
    oo = Object(True,True,2,[c,p])
    print(oo)
    shape_window.add_actor(oo)
    pyglet.app.run()