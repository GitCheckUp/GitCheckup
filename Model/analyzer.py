from Model import errordetection

def analyze_errors(irepo):
    for errorAlgorithm in errordetection.detectionAlgorithms:
        errorAlgorithm(irepo)
