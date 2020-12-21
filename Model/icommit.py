from Model import ifile, iauthor
from github import Github
commits = {}

def getCommit(commitData):
    sha = commitData.sha
    if (sha in commits):
        return commits[sha]
    else:
        newFile = ICommit(commitData)
        commits[sha] = newFile
        return newFile

class ICommit:
    def __init__(self, commitData):
        self.author = iauthor.getAuthor(commitData.author)
        self.committer = iauthor.getAuthor(commitData.committer)
        self.additions = commitData.stats.additions
        self.deletions = commitData.stats.deletions
        self.changes = commitData.stats.total
        self.sha = commitData.sha

        filesObject = commitData.files
        fileList = []
        for fileObject in list(filesObject):
            fileList.append(ifile.getFile(fileObject))

        self.files = fileList

        parentsObject = commitData.parents
        parentList = []
        for commitObject in list(parentsObject):
            parentList.append(getCommit(commitObject))

        self.parents = parentList
