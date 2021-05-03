from GitCheckup.Model import icommit

class IBranch:
    def __init__(self, branchData, icommitList = []):
        self.name = branchData.name
        self.headCommit = icommit.getCommit(branchData.commit)
        self.commitList = icommitList

    def updateCommitList(self,  icommitList):
        self.commitList = icommitList
