from github import Github
from View import usercli
from Controller.controller import Controller
from Model.database import Database
from Model.error import *
from Model import commit

#test
db = Database()
db.initialize_table_recent_repos()
db.add_to_recent_repos("deneme")


# Our Main View class, currently user-command line interface.
view = usercli.CommandLineView()

# The controller class
controller = Controller(view)

# Start running the program
controller.run()