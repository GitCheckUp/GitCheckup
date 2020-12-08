from github import Github
import re
import sqlite3
from database import *
#from database import db_op
# Our GitHub token for accessing the GitHub API
git_access = Github("bd0d1460b6fd6e9edc00926b1f6a2b9c8b8339f0")




# Method for parsing the repository address from the user and returns an appropriate string to get the repo from GitHub API
def get_repo_address():
    # address = input("Please enter repository address: ")
    address = "/GitCheckup/GitCheckup"
    address_split = address.split('//')

    address_blocks = [string.split('/') for string in address_split[1:]] if (len(address_split) > 1) else [string.split('/') for string in address_split]
    result_blocks = []
    for string_list in address_blocks:
        for string in string_list:
            result_blocks.append(string)

    if (result_blocks[0].lower() == "github.com" or result_blocks[0] == ''):
        del(result_blocks[0])

    if(len(result_blocks) != 2):
        raise(ValueError)

    result = result_blocks[0] + '/' + result_blocks[1]

    return result

def get_repository(repo_address):
    return git_access.get_repo(repo_address)


print("Welcome to GitCheckup!")

while(True):
    try:
        repo_address = get_repo_address()
    except:
        print("Could not read repository address, please enter a valid address.")
        continue

    try:
        repo = get_repository(repo_address)
        break
    except:
        print("Could not find a valid repository with this address. Please ensure there are no typos and the repository is public.")
        break

commits = repo.get_commits()

# DB test
DB = db_op()
db_op.initialize_table_recent_repos()



# branches = repo.get_branches()
# branches_list = list(branches)
# commit_list = list(commits)

# commit = commit_list[0]
# branch = branches_list[0]

# comments = commit.commit.message
# date = commit.commit.author.date
# files = commit.files

# mainc_commits = repo.get_commits("","main.c")
#print(list(mainc_commits))

# for mainc_commit in mainc_commits:
#     current = repo.get_contents("main.c",mainc_commit.sha)
   #print(current.decoded_content)
    #print("\n")

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
