import author
import file

commits = {}

def getCommit(commitData):
    sha = commitData.sha
    if (sha in commits):
        return commits[sha]
    else:
        newFile = Commit(commitData)
        commits[sha] = newFile
        return newFile

class Commit:
    def __init__(self, commitData):
        self.author = author.getAuthor(commitData.author)
        self.committer = author.getAuthor(commitData.committer)

        self.additions = commitData.stats.additions
        self.deletions = commitData.stats.deletions
        self.changes = commitData.stats.total
        self.sha = commitData.sha

        filesObject = commitData.files
        fileList = []
        for fileObject in list(filesObject):
            fileList.append(file.getFile(fileObject))

        self.files = fileList

        parentsObject = commitData.parents
        parentList = []
        for commitObject in list(parentsObject):
            parentList.append(getCommit(commitObject))

        self.parents = parentList

        commits[self.sha] = self
