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

def detect__dual__revert(irepo):

    errors = []
    error_id = 0

    for commit in irepo.commitList:
        message = commit.message

        #check if the current commit is a revert
        if (re.search("Revert \"", message) and re.search("This reverts commit", message)):
            # find the commit that was reverted
            reverted_commit_sha = re.search("(?<=This reverts commit )[\w]*", message).group(0)
            reverted_commit = irepo.commitDict[reverted_commit_sha]

            parent_message = reverted_commit.message

            #if parent is also a revert then error occurs
            if (re.search("Revert \"", parent_message) and re.search("This reverts commit", parent_message)):
                error = IError(error_id, 1, commit.committer, commit)
                errors.append(error)
                error_id += 1

    return errors

def detect__unnecessary__files(irepo):
    errors = []
    error_id = 0
    for c in irepo.commitList:
        for k in c.files:
            if(k.name in Config.unnecessary_file_names):
                print("FOUND.")
                print("--->" + k.name)
                error_detected = IError(error_id,2,c.committer,c)
                errors.append(error_detected)
                error_id += 1

    return errors
    #API dosyanin boyutunu vermiyor. Dolayisiyla 0byte dosya kontrolu yapamiyoruz.
    #Bu fonksiyon, IDE'lerin konfigurasyon dosyalarini tespit ediyor.
    #todo: Regex ile .idea klasorunun tamami ayiklanacak.

detectionAlgorithms = [detect__revert__mergecommit, detect__unnecessary__files]

def detect__originmaster__naming(irepo):
    errors = []
    error_id = 0

    for e in irepo.branchList:
        if e.name == "origin/master":
            detected_error = IError(error_id, 2, e.headCommit.comitter, e.headCommit.message)
            errors.append(detected_error)
            error_id += 1

    return errors
