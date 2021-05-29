from GitCheckup.Model.irepo import IRepo
from GitCheckup.Model.errordetection import *

class Model:
    def __init__(self):
        pass

    def get_repo(self, repo):
        return IRepo(repo)

    def analyze_errors(self, repo):
        return get_error_detections(repo)
