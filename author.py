authors = {}

def getAuthor(authorData):
    id = authorData.id
    if (id in authors):
        return authors[id]
    else:
        newAuthor = Author(authorData)
        authors[id] = newAuthor
        return newAuthor

class Author:
    def __init__(self, authorData):
        self.id = authorData.id
        self.name = authorData.name
        self.email = authorData.email