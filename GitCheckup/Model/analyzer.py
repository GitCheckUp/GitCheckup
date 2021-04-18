from GitCheckup.Model import errordetection

def analyze_errors(irepo):
    return errordetection.get_error_detections(irepo)
