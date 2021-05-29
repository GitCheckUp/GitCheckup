from View.application import Application
import threading
from View.usergui import GuiView
from Model import model
from Controller.controller import Controller
import sys
sys.path.append("..")


event = threading.Event()
event.func = None
event.args = None
model = model.Model()

# The controller class
controller = Controller(model, event)
controller.start()

# Our Main View class, currently user-command line interface.
application = Application(event, controller)
view = GuiView(event, application)

controller.set_view(view)

application.mainloop()

#controller.start_gui()
#controller.gui_analyze_repo()
#controller.welcome_user()
#controller.analyze_repo()






# DB test
# DB = Db_op()
# Db_op.initialize_table_recent_repos()
# Db_op.add_to_recent_repos("deneme.urlwr54")

# error.py test
# new_error = errors(0,1,15654)
# print(new_error.commit)

# ----------------------------

# branches = repo.get_branches()
# branches_list = list(branches)
# branch = branches_list[0]

# comments = commit.commit.message
# date = commit.commit.author.date
# files = commit.files

# mainc_commits = repo.get_commits("","main.c")
# print(list(mainc_commits))

# for mainc_commit in mainc_commits:
#     current = repo.get_contents("main.c",mainc_commit.sha)
# print(current.decoded_content)
# print("\n")

# branch = repo.get_branch("main")
# sad_sha = branch.commit.sha

# main_commits = repo.get_commits(sad_sha)

# for main_commit in main_commits:
#     print(main_commit)

# for file in files:
# print(file.status)
# print(file.filename, "additions:", file.additions, " deletions: ", file.deletions, " changes: ", file.changes)

# 95b69bfedb00f57db51c5b628ce4d132919eceaa

# print(comments)
# + commit messages
# + commit dates
# + commit files
# + commit file line count added, deleted, changed(added+deleted), same can be gotten for the commit (all files)
# + file status (added, removed, modified)
# + file modify/remove/add count
# + new files within a commit
# + all commits in a branch (goes all the way back to root)
# + start commit of a branch (performance heavy, have to subtract branch commits from all commits
# + code including comments (compare with prev codes). (get all commits for file, then get any version's code)
# - local commits
# + commits made by various users, commit comparison.
# + push date.
# + all the possible knowledge about the pushes and commits.
# + branch name.
# + people who works on a branch.
