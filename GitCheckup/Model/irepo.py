from GitCheckup.Model import icommit
from GitCheckup.Model import itag
from GitCheckup.Model.ibranch import IBranch

class IRepo:
    def __init__(self, repo):
        self.branchList = []
        self.commitList = []
        self.commitDict = {}
        self.tagList = []
        self.authorList = []

        try:
            master_branch = repo.get_branch("master")
            self.add_branch_commits(master_branch)
        except:
            try:
                main_branch = repo.get_branch("main")
                self.add_branch_commits(main_branch)
            except:
                pass

        for branch in repo.get_branches():
            if (branch.name != "master" and branch.name != "main"):
                self.add_branch_commits(branch)

        for tag_object in repo.get_tags():
            self.tagList.append(itag.ITag(tag_object, tag_object.commit))

    def add_branch_commits(self, branch):
        ibranch = IBranch(branch)
        self.branchList.append(ibranch)

        headCommit = branch.commit
        branch_commits = []
        frontier = [headCommit]

        while frontier.__len__():
            current_commit = frontier.pop(0)
            internal_commit = icommit.getCommit(current_commit)
            if (internal_commit.author not in self.authorList):
                self.authorList.append(internal_commit.author)
            internal_commit.set_parents(current_commit)

            if (internal_commit.sha not in self.commitDict):
                self.commitList.append(internal_commit)
                self.commitDict[internal_commit.sha] = internal_commit

                if (current_commit.parents.__len__()):
                    for parent in current_commit.parents:
                        if not (frontier.__contains__(parent)):
                            frontier.append(parent)

            branch_commits.append(internal_commit)

        ibranch.updateCommitList(branch_commits)
