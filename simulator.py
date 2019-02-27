import pyglet
import sys
from actor import *
from robot import *
from graph import *
"""
class Simulator(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        self.window = pyglet.window.Window.__init__(self)
        self.DIM = (500,500) 
        self.set_size(self.DIM[0], self.DIM[1])

        #set color
        pyglet.gl.glClearColor(0.10, 0.10, 0.0,0.0)
        #clear window
        self.clear()
        
        #get robot
        robot = SquareRobot()
        #track a list of actors
        self.actors = [robot]
        self.push_handlers(robot)
        # The game loop
        pyglet.clock.schedule_interval(self.update_actors, 1 / 60)
        pyglet.app.run()

    def on_draw(self):
        #print('Draw simulation')
        sys.stdout.flush()
        #clears out window
        self.clear()
        for actor in self.actors:
            actor.show()
    
    def update_actors(self, dt):
        for actor in self.actors:
            actor.update(dt)

if __name__ == '__main__':
    sim = Simulator()
"""
# Set up a window
#DIM = (800,600)
DIM = (200,200)
window = pyglet.window.Window(DIM[0], DIM[1])

# Initialize the player sprite
robot = SquareRobot()
actors = [robot]
obstacle = []

#equipt robot with magical sensor that sense things
s = Sensor(robot,obstacle,DIM)
robot.set_sensor(s)

#bedroom setup
#obs1 = Obs(shapes=[Rectangle(V(400,300),width=20,height=20)])
#obs2 = Obs(shapes=[Rectangle(V(700,300),width=20,height=20)])
#obs3 = Obs(shapes=[Rectangle(V(400,100),width=20,height=20)])
#obs4 = Obs(shapes=[Rectangle(V(700,100),width=20,height=20)])
#obs5 = Obs(shapes=[Rectangle(V(20,480),width=200,height=120)])
#actors.append(obs1)
#actors.append(obs2)
#actors.append(obs3)
#actors.append(obs4)
#actors.append(obs5)
#obstacle = [obs1,obs2,obs3,obs4,obs5];

#pass actor information to quadtree

#pass quadtree to robot

# Tell the main window that the player object responds to events
window.push_handlers(robot)

for actor in actors:
    if actor:
        print actor

@window.event
def on_draw():
    window.clear()
    for actor in actors:
            actor.show()


def update(dt):
    #print("update")
    for actor in actors:
            actor.update(dt,DIM,actors)




if __name__ == "__main__":
    # Update the game 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Tell pyglet to do its thing
    pyglet.app.run()
