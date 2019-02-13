import pyglet
from simulation.simulator import Simulator

if __name__ == "__main__":
	# Set up a window
	sim_window = Simulator()

	# Tell pyglet to do its thing
	pyglet.app.run()