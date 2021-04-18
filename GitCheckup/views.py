from django.http import HttpResponse
from django.shortcuts import render

import sys
sys.path.append(".")

from GitCheckup.Model.model import Model
from GitCheckup.Controller.controller import Controller
from github import Github

class Controller():
    def __init__(self, model):
        # Our GitHub token for accessing the GitHub API
        self.git_access = Github("bd0d1460b6fd6e9edc00926b1f6a2b9c8b8339f0")
        self.model = model

    # Method for parsing the repository address from the user and returns an appropriate string to get the repo from GitHub API
    def get_repo_address(self,repo_url=None):

        if(repo_url==None or repo_url ==""):
            address = "GitCheckUp/Demo"
        else:
            address = str(repo_url)
        address_split = address.split('//')

        address_blocks = [string.split('/') for string in address_split[1:]] if (len(address_split) > 1) else [
            string.split('/') for string in address_split]
        result_blocks = []
        for string_list in address_blocks:
            for string in string_list:
                result_blocks.append(string)

        if (result_blocks[0].lower() == "github.com" or result_blocks[0] == ''):
            del (result_blocks[0])

        if (len(result_blocks) != 2):
            raise (ValueError)

        result = result_blocks[0] + '/' + result_blocks[1]

        return result

    def get_repository(self, repo_address):
        return self.git_access.get_repo(repo_address)

    def analyze_repo(self, repo_url):
        try:
            repo_address = self.get_repo_address(repo_url)
        except:
            #self.view.display_error_repoAddress()
            return

        try:
            repo = self.get_repository(repo_address)
        except:
            #self.view.display_error_repoMissing()
            return

        #self.view.display_analyzing(repo_address)
        irepo = self.model.get_repo(repo)

        errorDetections = self.model.analyze_errors(irepo)

        totalErrorCount = 0
        for errorDetection in errorDetections:
            totalErrorCount += len(errorDetection.errorList)

        return errorDetections

    def errors_to_dict(self, errorObjects):
        dict = {}
        data = {}
        #{'data': {'Reverting': {'RevertMergeCommit': {'id_1': {'user': "Mehmet Kaan Özkan"}, 'id_2': {'user': "Anıl Güvenç"}}}}}

        for errorObject in errorObjects:
            errorData = {}
            errorInfos = {}

            for error in errorObject.errorList:
                errorDetails = {}

                errorDetails['error_type'] = error.error_type

                user = {}
                user['id'] = error.user.id
                user['url'] = error.user.url
                user['username'] = error.user.username
                user['name'] = error.user.name
                user['email'] = error.user.email

                errorDetails['user'] = user

                commit = {}

                commit['author'] = error.commit.author
                commit['committer'] = error.commit.committer
                commit['additions'] = error.commit.additions
                commit['deletions'] = error.commit.deletions
                commit['changes'] = error.commit.changes
                commit['sha'] = error.commit.sha
                commit['message'] = error.commit.message
                commit['date'] = error.commit.date

                errorDetails['commit'] = commit
                errorDetails['extra_info'] = error.extra_info

                errorInfos[error.error_id] = errorDetails

            errorData[errorObject.name] = errorInfos
            data[errorObject.category] = errorData

        dict['data'] = data
        return dict

model = Model()
controller = Controller(model)

def home(request):

    data = {}

    if request.method == "GET":
        repoName = request.GET.get("repo")
        errorDetections = controller.analyze_repo(repoName)

        data = controller.errors_to_dict(errorDetections)

    return render(request, 'GitCheckup/index.html', data)

def showMessage(request):
    return HttpResponse("Analyzed.")
