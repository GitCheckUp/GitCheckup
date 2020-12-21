from Model import errordetection
from Model.ierror import IError

class Analyzer:
    def __init__(self):
        pass

    def analyze_errors(self):
        for errorAlgorithm in errordetection.detectionAlgorithms:
            errorAlgorithm()