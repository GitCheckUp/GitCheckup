import os, sys, re
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from Model.ierror import IError
from Model.config import *

# IMPORTANT: When adding a new error detection, insert the class to the return list of the method at the bottom.

class ErrorDetection:
    def __init__(self, irepo):
        self.errorId = -1
        self.name = None
        self.category = None
        self.errorList = []

    def detect(self, irepo):
        pass

class ED_RevertMergeCommit(ErrorDetection):
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 0
        self.name = "RevertMergeCommit"
        self.category = "Reverting"
        self.errorList = []

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0
        for commit in irepo.commitList:
            message = commit.message

            # find all revert commits
            if (re.search("Revert \"", message) and re.search("This reverts commit", message)):
                # find the commit that was reverted
                reverted_commit_sha = re.search("(?<=This reverts commit )[\w]*", message).group(0)
                reverted_commit = irepo.commitDict[reverted_commit_sha]

                # if reverted commit has more than 1 parents, it is a merge commit, poor practice detected
                if (len(reverted_commit.parents) > 1):
                    error = IError(error_count, self.errorId, commit.committer, commit)
                    self.errorList.append(error)
                    error_count += 1

class ED_RevertRevertCommit(ErrorDetection):
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 1
        self.name = "RevertRevertCommit"
        self.category = "Reverting"
        self.errorList = []

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0

        for commit in irepo.commitList:
            message = commit.message

            # check if the current commit is a revert
            if (re.search("Revert \"", message) and re.search("This reverts commit", message)):
                # find the commit that was reverted
                reverted_commit_sha = re.search("(?<=This reverts commit )[\w]*", message).group(0)
                reverted_commit = irepo.commitDict[reverted_commit_sha]

                parent_message = reverted_commit.message

                # if parent is also a revert then error occurs
                if (re.search("Revert \"", parent_message) and re.search("This reverts commit", parent_message)):
                    error = IError(error_count, self.errorId, commit.committer, commit)
                    self.errorList.append(error)
                    error_count += 1

class ED_UnnecessaryFiles(ErrorDetection):
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 2
        self.name = "UnnecessaryFiles"
        self.category = "Creating Commits"
        self.errorList = []

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0
        for c in irepo.commitList:
            for k in c.files:
                if (k.name in Config.unnecessary_file_names):
                    error_detected = IError(error_count, self.errorId, c.committer, c, '('+k.name+')')
                    self.errorList.append(error_detected)
                    error_count += 1

        # API dosyanin boyutunu vermiyor. Dolayisiyla 0byte dosya kontrolu yapamiyoruz.
        # Bu fonksiyon, IDE'lerin konfigurasyon dosyalarini tespit ediyor.
        # todo: Regex ile .idea klasorunun tamami ayiklanacak.

class ED_OriginMasterBranchName(ErrorDetection):
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 3
        self.name = "OriginMasterBranchName"
        self.category = "Branching/Tagging"
        self.errorList = []

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0

        for e in irepo.branchList:
            if e.name == "origin/master":
                detected_error = IError(error_count, self.errorId, e.headCommit.comitter, e.headCommit.message)
                self.errorList.append(detected_error)
                error_count += 1

def get_error_detections(irepo, filter = "None"):
    if (filter == "None"):
        return [ED_RevertMergeCommit(irepo), ED_RevertRevertCommit(irepo), ED_UnnecessaryFiles(irepo), ED_OriginMasterBranchName(irepo)]
