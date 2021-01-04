files = {}
#from github import Github

def getFile(fileData,content,commit):
    sha = fileData.sha

    if (sha in files):
        return files[sha]
    else:
        newFile = File(fileData,content,commit)
        files[sha] = newFile
        return newFile

class File:
    def __init__(self, fileData,content,commit):
        self.additions = fileData.additions
        self.deletions = fileData.deletions
        self.changes = fileData.changes
        self.name = fileData.filename
        self.sha = fileData.sha
        self.status = fileData.status
        self.content = content
        self.commit = commit


        

