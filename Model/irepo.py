from icommit import ICommit
class IRepo:
    def __init__(self,repo):
        commits = repo.get_commits()
        commit_list = list(commits)
        myRepo = []
        for branch in repo.get_branches():
            internal_commit = ICommit.getCommit(branch.commit)
            current_branch = []
            current_commit = internal_commit
            current_branch.append(current_commit)
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
                if not (current_branch.__contains__(current_commit)):
                    current_branch.append(current_commit)
            self.myBranches.append(current_branch)