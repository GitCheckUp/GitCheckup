from typing import List
from Model.ibranch import IBranch
import unittest
from unittest.mock import patch
from unittest.mock import Mock
import Model.errordetection
import Model.irepo

class TestED_OriginMasterBranchName_Test(unittest.TestCase):

    def setUp(self):
        class mockedbranch:
             def __init__(self, name):
                self.name= name
        class mockedbranches:
             def __init__(self):
                 self.branchList = []
             def addBranch(self, name):
                 branch = mockedbranch(name)
                 self.branchList.append(branch)
        
        self.m = mockedbranches()
        self.m.addBranch("origin/origin/master")

    @patch('Model.irepo.IRepo')
    def test_ED_OriginMasterBranchName(self, mock_repo):
        mock_repo.return_value = self.m

        for e in Model.irepo.IRepo.branchList:
            print(e.name)
        for e in self.m.branchList:
            print(e.name)
        
        b=Model.errordetection.ED_OriginMasterBranchName(Model.irepo.IRepo)
        
        self.assertEqual(len(b.errorList), 0)

if __name__ == '__main__':
    unittest.main()