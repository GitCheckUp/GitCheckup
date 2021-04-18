from Model import icommit
from Model.ibranch import IBranch

class IRepo:
    def __init__(self,repo):
        self.branchList = []
        self.commitList = []
        self.commitDict = {}

        commits = repo.get_commits()

        #TODO: Does not actually give all commits, must fix
        for commit in list(commits):
            internal_commit = icommit.getCommit(commit)
            self.commitList.append(internal_commit)
            self.commitDict[internal_commit.sha] = internal_commit

        for branch in repo.get_branches():
            ibranch = IBranch(branch)
            self.branchList.append(ibranch)

        for branch in self.branchList:
            internal_commit = icommit.getCommit(branch.headCommit)
            branch_commits = []
            current_commit = internal_commit
            frontier = []

            if (current_commit.parents.__len__()):
                for parent in current_commit.parents:
                    frontier.append(parent)

            while frontier.__len__():
                current_commit = frontier[0]
                frontier.remove(frontier[0])
                if (current_commit.parents.__len__()):
                    for parent in current_commit.parents:
                        if not (frontier.__contains__(parent)):
                            frontier.append(parent)

                if not (branch_commits.__contains__(current_commit)):
                    branch_commits.append(current_commit)

            branch.updateCommitList(branch_commits)