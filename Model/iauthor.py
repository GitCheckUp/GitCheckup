authors = {}

def getAuthor(authorData):
    id = authorData.id
    if (id in authors):
        return authors[id]
    else:
        newAuthor = IAuthor(authorData)
        authors[id] = newAuthor
        return newAuthor

class IAuthor:
    def __init__(self, authorData):
        self.id = authorData.id
        self.name = authorData.name
        self.email = authorData.email