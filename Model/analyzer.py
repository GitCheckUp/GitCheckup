from Model import errordetection

def analyze_errors(irepo):
    for errorAlgorithm in errordetection.detectionAlgorithms:
        errors = errorAlgorithm(irepo)
        for ierror in errors:
            pass
            # print(ierror.user.name)
            # print(ierror.commit.sha)
