class File:
    def __init__(self, fileData):
        self.additions = fileData.additions
        self.deletions = fileData.deletions
        self.changes = fileData.changes
        self.name = fileData.filename
        self.sha = fileData.sha
        self.status = fileData.status