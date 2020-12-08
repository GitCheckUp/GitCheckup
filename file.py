files = {}

def getFile(fileData):
    sha = fileData.sha
    if (sha in files):
        return files[sha]
    else:
        newFile = File(fileData)
        files[sha] = newFile
        return newFile

class File:
    def __init__(self, fileData):
        self.additions = fileData.additions
        self.deletions = fileData.deletions
        self.changes = fileData.changes
        self.name = fileData.filename
        self.sha = fileData.sha
        self.status = fileData.status

        files[self.sha] = self
