from shape import *
import pyglet

class Actor():
    def __init__(self,shapes=None,actor_type=None):
       self.parts = shapes #the list of shapes
       self.actor_type = actor_type #what kind of actor are they?

    #print information
    def __repr__(self):
       s = "actor: "
       if self.actor_type:
            s += "actor_type: " + str(self.actor_type) + "| "
       if self.parts:
            for p in self.parts:
                s += str(p)
       return s

    #return all shapes/parts of the actor
    def get_parts(self):
       return self.parts

    #return actor type
    def get_actor_type(self):
       return self.actor_type

    #draw in 2D ############
    def show(self):
        for part in self.parts:
            if part.type == "polygon":
                v = part.get_pos()
                num = len(v)/2
                pyglet.graphics.draw(num, pyglet.gl.GL_POLYGON,
                ('v2i',v))

    #TODO translate is more like move fix in shape
    def move(self,vec,DIM):
       for p in self.parts:
            p.translate(vec)
       self.check_boundary(DIM)
    
    def check_boundary(self,DIM):
       for p in self.parts:
            vertices = p.get_vertices()
            for v in vertices:
                if v.x < 0:
                    p.translate((-v.x,0))
                if v.y < 0:
                    p.translate((0,-v.y))
                if v.x > DIM[0]:
                    p.translate((-v.x+DIM[0],0))
                if v.y > DIM[1]:
                    p.translate((0,-v.y+DIM[1]))


#specialized obstacle class
class Obs(Actor):
    def __init__(self,shapes=None):
        Actor.__init__(self,shapes,"obs")
    
    def update(self,dt,DIM):
      pass



if __name__ == '__main__':
    p1 = Polygon([V(0,0),V(1,0),V(1,1),V(0,1)])
    a = Obs([p1])
    print(a)
