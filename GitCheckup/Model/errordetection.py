import os, sys, re
import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from GitCheckup.Model.ierror import IError
from GitCheckup.Model.config import *

# IMPORTANT: When adding a new error detection, insert the class to the return list of the method at the bottom.


'''
Current config types,
avg_commit_day - average commit due date
workflow - which workflow should have been followed.
'''
user_config = {}

class ErrorDetection:
    def __init__(self, irepo):
        self.errorId = -1
        self.name = None
        self.message = None
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
        self.message = "This error refers to the poor practice where a merge commit is reverted. The outcome is often not well-understood by users and risks problems in the repository."
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
        self.message = "This error refers to the poor practice where a previous git revert commit is once again reverted. This does not remove history and clogs the repository with waste commits. An alternative is \'git reset\'"
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

                for parent_commit in reverted_commit.parents:

                    parent_message = parent_commit.message

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
        self.message = "This warning refers to unnecessary files being pushed alongside commits. This clogs the repository and potentially disrupts with other users\' IDE settings and etc. Try paying attention to the files being pushed."
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
        self.message = "This error refers to a branch name being equal to \'origin/master\' or \'origin/main\'. These will cause major confusion and problems as they refer to the main or master branch in the remote repository. Try paying attention to branch names."
        self.category = "Branching/Tagging"
        self.errorList = []
        self.is_warning = False

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0
        for e in irepo.branchList:
            if e.name == ("origin/origin/master" or "origin/origin/main"):
                detected_error = IError(error_count, self.errorId, e.headCommit.committer, e.headCommit, self.is_warning)
                self.errorList.append(detected_error)
                error_count += 1


class ED_HeadBranchName(ErrorDetection):
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 4
        self.name = "HeadBranchName"
        self.message = "This error refers to a branch name being equal to \'HEAD\'. This causes a major problem with git commands as head also refers to the head of the branch. Try paying attention to branch names."
        self.category = "Branching/Tagging"
        self.errorList = []
        self.is_warning = False

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0
        for e in irepo.branchList:
            if re.findall("/Head*|/head*|/HEAD*", e.name):
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
        self.message = "This warning refers to pushing too many file changes (deletions & additions) in a single commit. Commits that change too much in the code can be hard to follow and the commit messages may not accurately describe everything. Try breaking it into smaller chunks."
        self.category = "Creating Commits"
        self.errorList = []
        self.is_warning = True

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0
        if user_config['max_file'] == None:
            allowedchange = 5
        else:
            allowedchange = int(user_config['max_file'])
        for c in irepo.commitList:
            if(c.changes >= allowedchange):
                error_detected = IError(error_count, self.errorId, c.committer, c, self.is_warning, "(" + str(c.changes) + " changes)")
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
        self.message = "This error refers to commit messages that are not informative enough. Particularly, short messages (less than 3 words) may not be enough to accurately convey the changes. Try working more on the commit messages to inform everyone clearly."
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
        self.message = "This warning refers to commits being too infrequent and inconsistent. Either the commits may be too large, or the team may be pushing several commits at once but waiting a week or more. Try spreading out the commits and work more systematically."
        self.category = "Creating Commits"
        self.errorList = []
        self.is_warning = True

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0
        if (len(irepo.commitList) == 0):
            return



        """
        Here, we detect the infrequent commits
        """

        tripleTime = datetime.timedelta(int(user_config['avg_commit_day']))


        lastCommit = irepo.commitList[-1]

        for c in reversed(irepo.commitList):
            if (lastCommit == irepo.commitList[0]):
                timeBetween = datetime.timedelta(0)
            else:
                timeBetween = c.date - lastCommit.date

            lastCommit = c

            if (timeBetween > tripleTime):
                error_detected = IError(error_count, self.errorId, c.committer, c, self.is_warning, "(" + str(timeBetween) + " days)")
                self.errorList.append(error_detected)
                error_count += 1

class ED_KeepingOldBranches(ErrorDetection):
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 8
        self.name = "KeepingOldBranches"
        self.message = "This warning refers to old branches not being removed. This causes a growing pile of unnecessary data on the repository and should be removed."
        self.category = "Branching/Tagging"
        self.errorList = []
        self.is_warning = True

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0
        if user_config['branch_inactive_day'] == None:
            inactive_max_days = 15
        else:
            inactive_max_days = int(user_config['branch_inactive_day'])

        for branch in irepo.branchList:
            if ("main" not in branch.name and "master" not in branch.name):
                latest_commit_date = datetime.datetime(year = 1, month = 1, day = 1)
                current_commit = branch.commitList[0]

                for commit in branch.commitList:
                    if (commit.date > latest_commit_date):
                        latest_commit_date = commit.date
                        current_commit = commit

                if ((datetime.datetime.now() - latest_commit_date) > datetime.timedelta(days = inactive_max_days)):
                    detected_error = IError(error_count, self.errorId, current_commit.committer, current_commit, self.is_warning, "(" + branch.name + ")")
                    self.errorList.append(detected_error)
                    error_count += 1

class ED_OphanBranches(ErrorDetection):
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 9
        self.name = "OphanBranches"
        self.message = "This error refers to orphan branches in the repository. It is a better idea to create a different repository than having orphan branches."
        self.category = "Branching/Tagging"
        self.errorList = []
        self.is_warning = False

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0

        main_branch = None

        for branch in irepo.branchList:
            if ("main" in branch.name or "master" in branch.name):
                main_branch = branch
                break

        for branch in irepo.branchList:
            if ("main" not in branch.name and "master" not in branch.name):

                for commit in branch.commitList:
                    if (len(commit.parents) == 0):

                        first_commit = False
                        for main_commit in main_branch.commitList:
                            if (main_commit.sha == commit.sha):
                                first_commit = True
                                break

                        if (not first_commit):
                            detected_error = IError(error_count, self.errorId, commit.committer, commit, self.is_warning, "(" + branch.name + ")")
                            self.errorList.append(detected_error)
                            error_count += 1

class ED_CactusMissingTag(ErrorDetection):
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 10
        self.name = "CactusMissingTag"
        self.message = "This warning for Cactus Workflow refers to missing tags in the release branch. Untagged commits are possible, but only as bugfixes, otherwise the commit should be tagged."
        self.category = "Cactus Workflow"
        self.errorList = []
        self.is_warning = True

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0

        currentCommit = irepo.commitList[0]

        tag_commits_dict = {}
        for tag in irepo.tagList:
            tag_commits_dict[tag.commit.sha] = tag.commit

        for branch in irepo.branchList:
            if ("release" in branch.name):
                commits = branch.commitList
                for commit in commits:
                    if (commit.sha not in tag_commits_dict):
                        error_detected = IError(error_count, self.errorId, commit.committer, commit, self.is_warning)
                        self.errorList.append(error_detected)
                        error_count += 1

                break

class ED_CactusMissingReleaseBranch(ErrorDetection):
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 11
        self.name = "CactusMissingReleaseBranch"
        self.message = "This error for Cactus Workflow refers to the release branch not existing. Cactus Workflow requires one main and one release branch in the repository."
        self.category = "Cactus Workflow"
        self.errorList = []
        self.is_warning = False

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0

        found_release = False
        for branch in irepo.branchList:
            if ("release" in branch.name):
                found_release = True

        commit = irepo.branchList[0].commitList[0]
        if (not found_release):
            error_detected = IError(error_count, self.errorId, commit.committer, commit, self.is_warning)
            self.errorList.append(error_detected)
            error_count += 1

class ED_CactusUnnecessaryBranch(ErrorDetection):
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 12
        self.name = "CactusUnnecessaryBranch"
        self.message = "This error for Cactus Workflow refers to having other branches in the repository, apart from main/master and release. Remote branches are not allowed in Cactus Workflow, only local branches are allowed."
        self.category = "Cactus Workflow"
        self.errorList = []
        self.is_warning = False

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0

        if (len(irepo.branchList) > 2):
            for branch in irepo.branchList:
                if ("release" not in branch.name and "main" not in branch.name and "master" not in branch.name):
                    commit = branch.headCommit
                    error_detected = IError(error_count, self.errorId, commit.committer, commit, self.is_warning)
                    self.errorList.append(error_detected)
                    error_count += 1

class ED_CactusMergeIntoMain(ErrorDetection):
    def __init__(self, irepo):
        super().__init__(irepo)
        self.errorId = 13
        self.name = "CactusMergeIntoMain"
        self.message = "This error for Cactus Workflow refers to merge commits that merge with main/master branch. Cactus Workflow specifies that commits should be cherry-picked, not merged."
        self.category = "Cactus Workflow"
        self.errorList = []
        self.is_warning = False

        self.detect(irepo)

    def detect(self, irepo):
        error_count = 0

        found_release = False
        for branch in irepo.branchList:
            if ("main" in branch.name or "master" in branch.name):

                for commit in branch.commitList:
                    if (commit.message.startswith("Merge")):
                        error_detected = IError(error_count, self.errorId, commit.committer, commit, self.is_warning)
                        self.errorList.append(error_detected)
                        error_count += 1

def get_error_detections(irepo, user_conf,filter = "None"):
    if (filter == "None"):
        global user_config
        user_config = user_conf
        error_detections = []

        if user_config['revertMerge']:
            error_detections.append(ED_RevertMergeCommit(irepo))
        if user_config['revertRevert']:
            error_detections.append(ED_RevertRevertCommit(irepo))
        if user_config['unnecessaryFile']:
            error_detections.append(ED_UnnecessaryFiles(irepo))
        if user_config['originMaster']:
            error_detections.append(ED_OriginMasterBranchName(irepo))
        if user_config['headBranch']:
            error_detections.append(ED_HeadBranchName(irepo))
        if user_config['multipleFile']:
            error_detections.append(ED_MultipleFileChange(irepo))
        if user_config['uninformativeMessage']:
            error_detections.append(ED_UninformativeCommitMessage(irepo))
        if user_config['infrequentCommit']:
            error_detections.append(ED_InfrequentCommitFrequency(irepo))
        if user_config['keepingOldBranches']:
            error_detections.append(ED_KeepingOldBranches(irepo))
        if user_config['orphanBranches']:
            error_detections.append(ED_OphanBranches(irepo))


        if user_config['workflow'] == 'cactus':
            error_detections.append(ED_CactusMissingTag(irepo))
            error_detections.append(ED_CactusMissingReleaseBranch(irepo))
            error_detections.append(ED_CactusUnnecessaryBranch(irepo))
            error_detections.append(ED_CactusMergeIntoMain(irepo))

        return error_detections
