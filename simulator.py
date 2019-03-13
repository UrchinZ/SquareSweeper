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
width = robot_dim[0]*8  # 400
height = robot_dim[1]*6  #4  300
DIM = (width,height)

#equipt robot with magical sensor that sense things
s = Sensor(robot,obstacle,DIM)
robot.set_sensor(s)

#bedroom setup
obs1 = Obs(shapes=[Rectangle(V(350,120),width=20,height=20)])
obs2 = Obs(shapes=[Rectangle(V(200,120),width=20,height=20)])
obs3 = Obs(shapes=[Rectangle(V(350,10),width=20,height=20)])
obs4 = Obs(shapes=[Rectangle(V(200,10),width=20,height=20)])
obs5 = Obs(shapes=[Rectangle(V(0,215),width=140,height=85)])
actors.append(obs1)
actors.append(obs2)
actors.append(obs3)
actors.append(obs4)
actors.append(obs5)
obstacle = [obs1,obs2,obs3,obs4,obs5];

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
