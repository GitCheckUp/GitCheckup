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
        self.url = authorData.url
        self.username = self.getUsername(self.url)
        self.name = authorData.name
        self.email = authorData.email
    def getUsername(self,url):
        urlSplitted = url.split('/')
        return urlSplitted[-1]  #Returns the last part of the url, which is username.