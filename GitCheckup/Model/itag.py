from GitCheckup.Model import icommit

class ITag:
    def __init__(self, tag_object, commit):
        self.name = tag_object.name
        self.commit = icommit.getCommit(commit)
