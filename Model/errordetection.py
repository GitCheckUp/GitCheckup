import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from Model.ierror import IError
from Model.icommit import *
from Model.config import *
def detect__rebase__mergecommit(irepo):
    for branch in irepo.branchList:
        print(branch.name, ": ", branch.headCommit.sha)

    errors = []

    error1 = IError(0, 0, 12345678, branch.headCommit)
    error2 = IError(1, 0, 12345678, branch.headCommit.parents[0])

    errors.append(error1)
    errors.append(error2)

    return errors


def detect__unnecessary__files(irepo):
    for c in irepo.commitList:
        for k in c.files:
            if(k.name in Config.unnecessary_file_names):
                print("FOUND.")
                print("--->" + k.name)
                error_detected = IError(2,2,c.committer,c)
    #API dosyanin boyutunu vermiyor. Dolayisiyla 0byte dosya kontrolu yapamiyoruz.
    #Bu fonksiyon, IDE'lerin konfigurasyon dosyalarini tespit ediyor.
    #todo: Regex ile .idea klasorunun tamami ayiklanacak.
            

detectionAlgorithms = [detect__rebase__mergecommit,detect__unnecessary__files]

