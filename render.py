import pyglet
import sys

class ShapeWindow(pyglet.window.Window):

    def __init__(self,*args,**kwargs):
        pyglet.window.Window.__init__(self, *args,**kwargs)
        #clear window
        self.clear()
        #track a list of shapes
        self.shapes = []

    def on_draw(self):
        print('Draw simulation')
        sys.stdout.flush()

        self.draw_points()
        self.draw_line()
        self.draw_triangle()
        self.draw_polygon()

    def draw_points(self):
        pyglet.graphics.draw(3, pyglet.gl.GL_POINTS,
        ('v2i', (10, 10, 100, 100, 200,200)))

    def draw_line(self):
        pyglet.graphics.draw(4, pyglet.gl.GL_LINES,
        ('v2i', (10, 100, 50, 50, 200,100,300,300)))

    def draw_triangle(self):
        pyglet.graphics.draw(3, pyglet.gl.GL_TRIANGLES,
        ('v2i', (500, 100, 600, 300, 550,450)))

    def draw_polygon(self):
        pyglet.graphics.draw(7, pyglet.gl.GL_POLYGON,
        ('v2i', (100, 400, 150, 350, 200,400,250,350,300,450,250,375,200,450)))

if __name__ == '__main__':
    shape_window = ShapeWindow()
    pyglet.app.run()