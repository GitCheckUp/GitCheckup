from Model import analyzer
from Model.irepo import IRepo

class Model:
    def __init__(self):
        pass

    def get_repo(self, repo):
        return IRepo(repo)

    def analyze_errors(self, repo):
        analyzer.analyze_errors(repo)