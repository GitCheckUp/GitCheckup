import os, sys, re
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from Model.ierror import IError
from Model.config import *


def detect__revert__mergecommit(irepo):
    errors = []
    error_id = 0
    for commit in irepo.commitList:
        message = commit.message

        # find all revert commits
        if (re.search("Revert \"", message) and re.search("This reverts commit", message)):
            # find the commit that was reverted
            reverted_commit_sha = re.search("(?<=This reverts commit )[\w]*", message).group(0)
            reverted_commit = irepo.commitDict[reverted_commit_sha]

            # if reverted commit has more than 1 parents, it is a merge commit, poor practice detected
            if(len(reverted_commit.parents) > 1):
                error = IError(error_id, 0, commit.committer, commit)
                errors.append(error)
                error_id += 1

    return errors

def detect__unnecessary__files(irepo):
    errors = []
    error_id = 0

    for commit in irepo.commitList:
        for file in commit.files:
            if(file.name in config.unnecessary_file_names):
                print("amk")
            if(file.content.size <= 300):
                print("aaamk2")
"""
    #Investigate all the files in the repository:
    contents = irepo.repo_itself.get_contents("")
    while(contents):
        file_content = contents.pop(0)
        if(file_content.type == "dir"):  #Look into directories
            contents.extend(irepo.repo_itself.get_contents(file_content.path))
        else:
            if(file_content.name in Config.unnecessary_file_names):
                error_detected = IError(error_id, 1, c.committer, c)   #Error id=1, IDE config file found.
                errors.append(error_detected)
                error_id += 1
                print(file_content.name)
            if(file_content.size <= 8):
                error_detected = IError(error_id, 2, c.committer, c)  # Error id=2, 0 byte file found.
                errors.append(error_detected)
                error_id += 1
                print(file_content.name)

            print(str(file_content.name) +": size -->"+ str(file_content.size))
"""

detectionAlgorithms = [detect__revert__mergecommit, detect__unnecessary__files]

