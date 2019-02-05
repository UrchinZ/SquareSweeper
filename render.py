import pyglet
import sys
from actor import *

class ShapeWindow(pyglet.window.Window):

    def __init__(self,*args,**kwargs):
        pyglet.window.Window.__init__(self, *args,**kwargs)
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
                if(shape.get_type() == "circle"):
                    print("I need a circle function")
                else: #for now definitely polygon
                    print("drawing polygon")
                    v = shape.get_v()
                    print(v)
                    num = len(v)
                    print(num)

                    self.draw_polygon(num,v)

        #self.draw_points()
        #self.draw_line()
        #self.draw_triangle()
        #self.draw_polygon()

    def draw_points(self):
        pyglet.graphics.draw(3, pyglet.gl.GL_POINTS,
        ('v2i', (10, 10, 100, 100, 200,200)))

    def draw_line(self):
        pyglet.graphics.draw(4, pyglet.gl.GL_LINES,
        ('v2i', (10, 100, 50, 50, 200,100,300,300)))

    def draw_triangle(self):
        pyglet.graphics.draw(3, pyglet.gl.GL_TRIANGLES,
        ('v2i', (500, 100, 600, 300, 550,450)))

    def draw_polygon(self,num,v):
        flat_list = []
        for l in v:
            t = l.coords()
            flat_list.extend(list(t))
        t  = tuple(flat_list)
        print(t)
        pyglet.graphics.draw(num, pyglet.gl.GL_POLYGON,
        ('v2i',t))

    def update(self, dt):
        pass
if __name__ == '__main__':
    shape_window = ShapeWindow()
    c = Circle(V(1,1),1)
    print(c)
    p = Polygon([V(300,400),V(200,200),V(200,300)])
    print(p)
    print("first object")
    oo = Object(True,True,2,[c,p])
    print(oo)
    shape_window.add_actor(oo)
    pyglet.app.run()