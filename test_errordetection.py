import datetime
from typing import List
from GitCheckup.Model.ibranch import IBranch
import unittest
from unittest.mock import patch
from unittest.mock import Mock
import GitCheckup.Model.errordetection
import GitCheckup.Model.irepo
import GitCheckup.Model.ierror
import GitCheckup.Model.iauthor
import GitCheckup.Model.icommit

class mockedTag:
    def __init__(self):
        self.commit = mockedcommit()

class mockedbranch:
     def __init__(self, name):
        self.name= name
        self.headCommit = mockedcommit()
        self.commitList = []

     def comitter(self):
        return ' '

class mockedfile:
     def __init__(self, name):
        self.name = name

class mockedcommit:
     def __init__(self):
         self.name= ' '
         self.committer= ' '
         self.message = ""
         self.files = []
         self.date = 0
         self.parents = []
         self.sha = 0
     def addFile(self, name):
         file = mockedfile(name)
         self.files.append(file)
     def addParent(self):
         commit = mockedcommit()
         self.parents.append(commit)
                
class mockedbranches:
     def __init__(self):
         self.branchList = []
         self.commitList = []
         self.commitDict = {}
         self.tagList = []
     def addBranch(self, name):
         branch = mockedbranch(name)
         self.branchList.append(branch)
     def addCommit(self):
         commit = mockedcommit()
         self.commitList.append(commit)

         

class TestED_RevertMergeCommit(unittest.TestCase):

    irepo = mockedbranches()
    irepo.addCommit()
    irepo.commitList[0].message = "Revert \" This reverts commit 123456"
    irepo.commitList[0].addParent()
    irepo.commitList[0].addParent()
    irepo.commitDict['123456'] = irepo.commitList[0]


    def test_ED_RevertMergeCommit(self):
        
        b=GitCheckup.Model.errordetection.ED_RevertMergeCommit(self.irepo)
        
        self.assertEqual(len(b.errorList), 1)

    def test_ED_RevertMergeCommit_Reverse(self):
        self.irepo.commitList.clear()
        b=GitCheckup.Model.errordetection.ED_RevertMergeCommit(self.irepo)
        
        self.assertEqual(len(b.errorList), 0)

class TestED_RevertRevertCommit(unittest.TestCase):

    irepo = mockedbranches()
    irepo.addCommit()
    irepo.commitList[0].message = "Revert \" This reverts commit 123456"
    irepo.commitList[0].addParent()
    irepo.commitList[0].parents[0].message = "Revert \" This reverts commit 234567"
    irepo.commitDict['123456'] = irepo.commitList[0]


    def test_ED_RevertRevertCommit(self):
        
        b=GitCheckup.Model.errordetection.ED_RevertRevertCommit(self.irepo)
        
        self.assertEqual(len(b.errorList), 1)

    def test_ED_RevertRevertCommit_Reverse(self):

        self.irepo.commitList[0].parents[0].message = "Pattern change"

        b=GitCheckup.Model.errordetection.ED_RevertRevertCommit(self.irepo)
        
        self.assertEqual(len(b.errorList), 0)

class TestED_UnnecessaryFiles(unittest.TestCase):

    irepo = mockedbranches()
    irepo.addCommit()
    irepo.commitList[0].addFile(".DS_Store")

    def test_ED_UnnecessaryFiles(self):
        
        b=GitCheckup.Model.errordetection.ED_UnnecessaryFiles(self.irepo)
        
        self.assertEqual(len(b.errorList), 1)

    def test_ED_UnnecessaryFiles_Reverse(self):

        self.irepo.commitList.clear()

        b=GitCheckup.Model.errordetection.ED_UnnecessaryFiles(self.irepo)
        
        self.assertEqual(len(b.errorList), 0)


class TestED_OriginMasterBranchName(unittest.TestCase):

    irepo = mockedbranches()
    irepo.addBranch("origin/origin/master")
    irepo.addBranch("origin/pattern_change")

    def test_ED_OriginMasterBranchName(self):

        b=GitCheckup.Model.errordetection.ED_OriginMasterBranchName(self.irepo)
        
        self.assertEqual(len(b.errorList), 1)

    def test_ED_OriginMasterBranchName_Reverse(self):

        self.irepo.branchList.clear()

        b=GitCheckup.Model.errordetection.ED_OriginMasterBranchName(self.irepo)
        
        self.assertEqual(len(b.errorList), 0)

class TestED_HeadBranchName(unittest.TestCase):

    irepo = mockedbranches()
    irepo.addBranch("/head/")
    irepo.addBranch("origin/pattern_change")

    def test_ED_HeadBranchName(self):

        b=GitCheckup.Model.errordetection.ED_HeadBranchName(self.irepo)
        
        self.assertEqual(len(b.errorList), 1)
    
    def test_ED_HeadBranchName_Reverse(self):

        self.irepo.branchList.clear()

        b=GitCheckup.Model.errordetection.ED_HeadBranchName(self.irepo)
        
        self.assertEqual(len(b.errorList), 0)

class TestED_MultipleFileChange(unittest.TestCase):

    irepo = mockedbranches()
    irepo.addCommit()
    irepo.commitList[0].additions = 3
    irepo.commitList[0].deletions = 3


    def test_ED_MultipleFileChange(self):

        GitCheckup.Model.errordetection.user_config['max_file'] = None

        b=GitCheckup.Model.errordetection.ED_MultipleFileChange(self.irepo)
        
        self.assertEqual(len(b.errorList), 1)

    def test_ED_MultipleFileChange_Reverse(self):

        self.irepo.commitList[0].additions = 2
        self.irepo.commitList[0].deletions = 2

        GitCheckup.Model.errordetection.user_config['max_file'] = None
        
        b=GitCheckup.Model.errordetection.ED_MultipleFileChange(self.irepo)
        
        self.assertEqual(len(b.errorList), 0)

class TestED_UninformativeCommitMessage(unittest.TestCase):

    irepo = mockedbranches()
    irepo.addCommit()
    irepo.commitList[0].message = "Done smth"


    def test_ED_UninformativeCommitMessage(self):
        
        b=GitCheckup.Model.errordetection.ED_UninformativeCommitMessage(self.irepo)
        
        self.assertEqual(len(b.errorList), 1)
    
    def test_ED_UninformativeCommitMessage_Reverse(self):

        self.irepo.commitList[0].message = "Changed the pattern of a workflow in code"
        
        b=GitCheckup.Model.errordetection.ED_UninformativeCommitMessage(self.irepo)
        
        self.assertEqual(len(b.errorList), 0)

class TestED_InfrequentCommitFrequency(unittest.TestCase):

    irepo = mockedbranches()
    irepo.addCommit()
    irepo.commitList[0].date = datetime.timedelta(4)
    irepo.addCommit()
    irepo.commitList[1].date = datetime.timedelta(0)


    def test_ED_InfrequentCommitFrequency(self):

        GitCheckup.Model.errordetection.user_config['avg_commit_day'] = "3"

        b=GitCheckup.Model.errordetection.ED_InfrequentCommitFrequency(self.irepo)
        
        self.assertEqual(len(b.errorList), 1)
    
    def test_ED_InfrequentCommitFrequency_Reverse(self):

        GitCheckup.Model.errordetection.user_config['avg_commit_day'] = "5"
        
        b=GitCheckup.Model.errordetection.ED_InfrequentCommitFrequency(self.irepo)
        
        self.assertEqual(len(b.errorList), 0)

class TestED_CactusMissingTag(unittest.TestCase):

    irepo = mockedbranches()
    irepo.tagList.append(mockedTag())
    irepo.tagList[0].commit= mockedcommit()
    irepo.tagList[0].commit.sha = "123456"
    irepo.addBranch("release")
    irepo.addCommit()
    irepo.branchList[0].commitList.append(mockedcommit())
    irepo.branchList[0].commitList[0].sha = "234567"

    def test_ED_CactusMissingTag(self):
        
        b=GitCheckup.Model.errordetection.ED_CactusMissingTag(self.irepo)
        
        self.assertEqual(len(b.errorList), 1)

    def test_ED_CactusMissingTag_Reverse(self):
        
        self.irepo.branchList[0].commitList[0].sha = "123456"

        b=GitCheckup.Model.errordetection.ED_CactusMissingTag(self.irepo)
        
        self.assertEqual(len(b.errorList), 0)

class TestED_CactusMissingReleaseBranch(unittest.TestCase):

    irepo = mockedbranches()
    irepo.addBranch("Pattern_v2")
    irepo.branchList[0].commitList.append(mockedcommit())

    def test_ED_CactusMissingReleaseBranch(self):
        
        b=GitCheckup.Model.errordetection.ED_CactusMissingReleaseBranch(self.irepo)
        
        self.assertEqual(len(b.errorList), 1)

    def test_ED_CactusMissingReleaseBranch_Reverse(self):
        
        self.irepo.addBranch("release")
        self.irepo.branchList[1].commitList.append(mockedcommit())

        b=GitCheckup.Model.errordetection.ED_CactusMissingReleaseBranch(self.irepo)
        
        self.assertEqual(len(b.errorList), 0)

class TestED_CactusUnnecessaryBranch(unittest.TestCase):

    irepo = mockedbranches()
    irepo.addBranch("release")
    irepo.addBranch("Pattern_v2")
    irepo.addBranch("main")
    irepo.branchList[0].commitList.append(mockedcommit())

    def test_ED_CactusUnnecessaryBranch(self):
        
        b=GitCheckup.Model.errordetection.ED_CactusUnnecessaryBranch(self.irepo)
        
        self.assertEqual(len(b.errorList), 1)
    
    def test_ED_CactusUnnecessaryBranch_Reverse(self):
        
        self.irepo.branchList.clear()
        self.irepo.addBranch("release")
        self.irepo.addBranch("release")
        self.irepo.addBranch("main")

        b=GitCheckup.Model.errordetection.ED_CactusUnnecessaryBranch(self.irepo)
        
        self.assertEqual(len(b.errorList), 0)



class TestED_CactusMergeIntoMain(unittest.TestCase):

    

    irepo = mockedbranches()
    irepo.addBranch("main")
    irepo.branchList[0].commitList.append(mockedcommit())
    irepo.branchList[0].commitList[0].message = "Merged to Pattern_v2 branch"

    def test_ED_CactusMergeIntoMain(self):
        
        b=GitCheckup.Model.errordetection.ED_CactusMergeIntoMain(self.irepo)
        
        self.assertEqual(len(b.errorList), 1)
    
    def test_ED_CactusMergeIntoMain_Reverse(self):
        
        self.irepo.branchList[0].commitList[0].message = "Changed the pattern of a workflow in code"

        b=GitCheckup.Model.errordetection.ED_CactusMergeIntoMain(self.irepo)
        
        self.assertEqual(len(b.errorList), 0)



if __name__ == '__main__':
    unittest.main()