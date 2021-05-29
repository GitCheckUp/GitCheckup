from GitCheckup.Model import ifile, iauthor
commits = {}

def getCommit(commitData):
    sha = commitData.sha
    if (sha == None):
        return None
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
        self.message = commitData.commit.message
        self.date = commitData.commit.author.date

        filesObject = commitData.files
        fileList = []
        for fileObject in list(filesObject):
            fileList.append(ifile.getFile(fileObject))

        self.files = fileList

    def set_parents(self, commitData):
        parentList = []
        for commitObject in list(commitData.parents):
            parentList.append(getCommit(commitObject))

        self.parents = parentList
