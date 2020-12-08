from author import Author
from file import File

class Commit:
    def __init__(self, commitData):
        self.author = Author(commitData.author)
        self.committer = Author(commitData.committer)
        self.additions = commitData.stats.additions
        self.deletions = commitData.stats.deletions
        self.changes = commitData.stats.total
        self.sha = commitData.sha

        filesObject = commitData.files
        fileList = []
        for file in list(filesObject):
            fileList.append(File(file))

        self.files = fileList

        parentsObject = commitData.parents
        parentList = []
        for commit in list(parentsObject):
            parentList.append(Commit(commit))

        self.parents = parentList



