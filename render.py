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
        
        print("args:")
        for arg in args:
            print(arg)

        print("kwargs:")
        for key, value in kwargs.iteritems():
            print(str(key) + " " + str(value))

        if "width" in kwargs and "height" in kwargs:
            self.set_size(int(kwargs.get("width")), int(kwargs.get("height")))

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
        #clears out window
        self.clear()

        for a in self.actors:
            for shape in a.get_pieces():
                v = shape.show()
                if(shape.get_type() == "circle"):
                    self.draw_circle(v)
                else: #for now definitely polygon
                    self.draw_polygon(v)

    #allow keyboard control
    #need to refactor this...
    def on_key_press(self,key,modifiers):
        moving = 50
        if key == pyglet.window.key.UP:
            print("up")
            for a in self.actors:
                if a.movable:
                    a.up(moving)
        elif key == pyglet.window.key.DOWN:
            print("down")
            for a in self.actors:
                if a.movable:
                    a.down(moving)
        elif key == pyglet.window.key.RIGHT:
            print("right")
            for a in self.actors:
                if a.movable:
                    a.right(moving)
        elif key == pyglet.window.key.LEFT:
            print("left")
            for a in self.actors:
                if a.movable:
                    a.left(moving)

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
        print(dt)
        pass


if __name__ == '__main__':
    shape_window = ShapeWindow(width=400, height=400)
    c = Circle(V(1,1),100)
    print(c)
    p = Polygon([V(300,400),V(200,200),V(200,300)])
    print(p)

    
    print("first object")
    oo = Object(False,True,2,[c,p])
    print(oo)

    r = Polygon([V(0,0),V(100,0),V(100,100),V(0,100)])
    robot = Object(True,False,1,[r])

    shape_window.add_actor(oo)
    shape_window.add_actor(robot)
    pyglet.app.run()