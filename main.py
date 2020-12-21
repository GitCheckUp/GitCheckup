from View import usercli
from Controller.controller import Controller
import sys
sys.path.append("..")

# Our Main View class, currently user-command line interface.
view = usercli.CommandLineView()

# The controller class
controller = Controller(view)

# Start running the program
controller.run()