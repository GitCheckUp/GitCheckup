from github import Github
from database import *
from View import usercli
from Controller.controller import Controller
from error import *
from Model import commit

# Our Main View class, currently user-command line interface.
view = usercli.CommandLineView()

# The controller class
controller = Controller(view)

# Start running the program
controller.run()