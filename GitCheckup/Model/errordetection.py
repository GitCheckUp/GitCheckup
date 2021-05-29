import os, sys, re
import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from GitCheckup.Model.ierror import IError
from GitCheckup.Model.config import *

# IMPORTANT: When adding a new error detection, insert the class to the return list of the method at the bottom.

user_config = {}

class ErrorDetection:
    def __init__(self, irepo):
        self.errorId = -1
        self.name = None
        self.category = None
        self.errorList = []
        self.is_warning = False

    def detect(self, irepo):
        pass

class ED_RevertMergeCommit(ErrorDetection):
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 0
        self.name = "RevertMergeCommit"
        self.category = "Reverting"
        self.errorList = []
        self.is_warning = False

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
                    error = IError(error_count, self.errorId, commit.committer, commit, self.is_warning)
                    self.errorList.append(error)
                    error_count += 1

class ED_RevertRevertCommit(ErrorDetection):
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 1
        self.name = "RevertRevertCommit"
        self.category = "Reverting"
        self.errorList = []
        self.is_warning = False

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
                    error = IError(error_count, self.errorId, commit.committer, commit, self.is_warning)
                    self.errorList.append(error)
                    error_count += 1

class ED_UnnecessaryFiles(ErrorDetection):
    """
    Check if the user commited any unnecessary file, such as IDE configuration files.
    """
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 2
        self.name = "UnnecessaryFiles"
        self.category = "Creating Commits"
        self.errorList = []
        self.is_warning = True

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0
        for c in irepo.commitList:
            for k in c.files:
                if any(re.compile(regex).match(k.name) for regex in Config.unnecessary_files_regex):
                    error_detected = IError(error_count, self.errorId, c.committer, c, self.is_warning, '('+k.name+')')
                    self.errorList.append(error_detected)
                    error_count += 1

class ED_OriginMasterBranchName(ErrorDetection):
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 3
        self.name = "OriginMasterMainBranchName"
        self.category = "Branching/Tagging"
        self.errorList = []
        self.is_warning = False

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0
        for e in irepo.branchList:
            if e.name == "origin/origin/master" or "origin/origin/main":
                detected_error = IError(error_count, self.errorId, e.headCommit.committer, e.headCommit, self.is_warning)
                self.errorList.append(detected_error)
                error_count += 1


class ED_HeadBranchName(ErrorDetection):
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 4
        self.name = "HeadBranchName"
        self.category = "Branching/Tagging"
        self.errorList = []
        self.is_warning = False

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0
        for e in irepo.branchList:
            if re.findall("/Head$|/head$|/HEAD$", e.name):
                detected_error = IError(error_count, self.errorId, e.headCommit.committer, e.headCommit, self.is_warning)
                self.errorList.append(detected_error)
                error_count += 1

class ED_MultipleFileChange(ErrorDetection):
    """
    Check if the user commited multiple changes.
    """
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 5
        self.name = "MultipleFileCommits"
        self.category = "Creating Commits"
        self.errorList = []
        self.is_warning = True

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0
        for c in irepo.commitList:
            if(c.additions + c.deletions >= 5):
                error_detected = IError(error_count, self.errorId, c.committer, c, self.is_warning)
                self.errorList.append(error_detected)
                error_count += 1

class ED_UninformativeCommitMessage(ErrorDetection):
    """
    Check if the user wrote a commit message less then three words. The message also includes commit title.
    """
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 6
        self.name = "UninformativeComment"
        self.category = "Creating Commits"
        self.errorList = []
        self.is_warning = False

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0
        for c in irepo.commitList:
            if(c.message.count(' ') <3):
                error_detected = IError(error_count, self.errorId, c.committer, c, self.is_warning)
                self.errorList.append(error_detected)
                error_count += 1

class ED_InfrequentCommitFrequency(ErrorDetection):
    """
    Finds average time between subsequent commits, suppose as t.
    If there is a time of 3t or more between commits, marks it as infrequent commit.
    Same if t > 7 days.
    """
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 7
        self.name = "InfrequentCommitFrequency"
        self.category = "Creating Commits"
        self.errorList = []
        self.is_warning = True

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0
        if (len(irepo.commitList) == 0):
            return

        """
        Here, calculate the average time taken.
        """
        totalTime = datetime.timedelta()
        lastCommit = irepo.commitList[-1]

        for c in reversed(irepo.commitList):
            if (lastCommit == irepo.commitList[-1]):
                timeBetween = datetime.timedelta()
            else:
                timeBetween = c.date - lastCommit.date

            totalTime += timeBetween
            lastCommit = c

        """
        Here, we detect the infrequent commits
        """


        print("User input is :",int(user_config['avg_commit_day']))

        tripleTime = datetime.timedelta(int(user_config['avg_commit_day']))


        lastCommit = irepo.commitList[-1]

        for c in reversed(irepo.commitList):
            if (lastCommit == irepo.commitList[-1]):
                timeBetween = datetime.timedelta()
            else:
                timeBetween = c.date - lastCommit.date

            lastCommit = c

            if (timeBetween > tripleTime):
                error_detected = IError(error_count, self.errorId, c.committer, c, self.is_warning)
                self.errorList.append(error_detected)
                error_count += 1


class ED_MultiplePushInsteadOne(ErrorDetection):
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 8
        self.name = "MultiplePush"
        self.category = "Pushing Commits"
        self.errorList = []
        self.is_warning = True

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0

        currentCommit = irepo.commitList[0]
        for commit in irepo.commitList[1:]:
            if currentCommit.author.id == commit.author.id:

                time_delta = (currentCommit.date - commit.date)
                total_seconds = time_delta.total_seconds()
                minutes = total_seconds / 60

                if minutes <= 5:
                    error_detected = IError(error_count, self.errorId, commit.committer, commit, self.is_warning)
                    self.errorList.append(error_detected)
                    error_count += 1

            currentCommit = commit

def get_error_detections(irepo,user_conf,filter = "None"):

    global user_config
    user_config = user_conf

    if (filter == "None"):
        return [ED_RevertMergeCommit(irepo), ED_RevertRevertCommit(irepo), ED_UnnecessaryFiles(irepo), ED_OriginMasterBranchName(irepo), ED_HeadBranchName(irepo), ED_MultipleFileChange(irepo), ED_UninformativeCommitMessage(irepo), ED_InfrequentCommitFrequency(irepo),ED_MultiplePushInsteadOne(irepo)]
