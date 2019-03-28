import pyglet
import sys
from actor import *
from robot import *
from graph import *

# Initialize the player sprite
robot = SquareRobot()
actors = [robot]
robot_dim = robot.get_dim()
obstacle = []

#making life easier
#setting window dimension
width = robot_dim[0]*4  # 400
height = robot_dim[1]*4  #4  300
DIM = (width,height)


#bedroom setup
#obs1 = Obs(shapes=[Rectangle(V(365,130),width=20,height=20)])
#obs2 = Obs(shapes=[Rectangle(V(175,130),width=20,height=20)])
#obs3 = Obs(shapes=[Rectangle(V(365,15),width=20,height=20)])
#obs4 = Obs(shapes=[Rectangle(V(175,15),width=20,height=20)])
#obs5 = Obs(shapes=[Rectangle(V(0,275),width=120,height=75)])
#actors.append(obs1)
#actors.append(obs2)
#actors.append(obs3)
#actors.append(obs4)
#actors.append(obs5)
#obstacle = [obs1,obs2,obs3,obs4,obs5];


obs1 = Obs(shapes=[Rectangle(V(102,102),width=20,height=20)])
obstacle = [obs1]
actors.append(obs1)

#equipt robot with magical sensor that sense things
s = Sensor(robot,obstacle,DIM)
robot.set_sensor(s)

window = pyglet.window.Window(DIM[0], DIM[1])

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
