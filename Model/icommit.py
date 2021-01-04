from Model import ifile, iauthor
commits = {}

def getCommit(commitData,repo=None):
    sha = commitData.sha
    if (sha in commits and repo==None):
        return commits[sha]
    else:
        newFile = ICommit(commitData,repo)
        commits[sha] = newFile
        return newFile

class ICommit:
    def __init__(self, commitData,repo):
        self.author = iauthor.getAuthor(commitData.author)
        self.committer = iauthor.getAuthor(commitData.committer)
        self.additions = commitData.stats.additions
        self.deletions = commitData.stats.deletions
        self.changes = commitData.stats.total
        self.sha = commitData.sha
        self.message = commitData.commit.message
        self.repo = repo

        filesObject = commitData.files
        commitFiles = list(filesObject)

        fileList = []

        contents = self.repo.get_contents("")
        while (contents):
            file_content = contents.pop(0)
            if (file_content.type == "dir"):  # Look into directories
                contents.extend(self.repo.get_contents(file_content.path))
            else:
                for i in commitFiles:     #Compare each File object in commit, then append related ContentFile to iFile
                    if(file_content.sha==i.sha):
                        fileList.append(ifile.getFile(i,file_content,self))
                        print(file_content.name)

        self.files = fileList

        parentsObject = commitData.parents
        parentList = []
        for commitObject in list(parentsObject):
            parentList.append(getCommit(commitObject,self.repo))

        self.parents = parentList
