from Model.ierror import IError

def detect__rebase__mergecommit(irepo):
    for branch in irepo.branchList:
        print(branch.name, ": ", branch.headCommit.sha)

    errors = []

    error1 = IError(0, 0, 12345678, branch.headCommit)
    error2 = IError(1, 0, 12345678, branch.headCommit.parents[0])

    errors.append(error1)
    errors.append(error2)

    return errors

detectionAlgorithms = [detect__rebase__mergecommit]