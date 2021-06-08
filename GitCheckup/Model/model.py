from GitCheckup.Model.irepo import IRepo
from GitCheckup.Model.errordetection import *

class Model:
    def __init__(self):
        self.errorDetections = None
        self.irepo = None
        pass

    def create_irepo(self, repoObject):
        self.irepo = IRepo(repoObject)

    def analyze_errors(self, repo, user_config):
        return get_error_detections(repo,user_config)
