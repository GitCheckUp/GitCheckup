from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from .utils import get_plot
import sys

sys.path.append(".")

from GitCheckup.Model.model import Model
from GitCheckup.Model.config import config
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

    def analyze_repo(self, repo_url,user_config):
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

        errorDetections = self.model.analyze_errors(irepo,user_config)

        totalErrorCount = 0
        for errorDetection in errorDetections:
            totalErrorCount += len(errorDetection.errorList)

        return errorDetections

    def errors_to_dict(self, errorObjects):
        data = {}
        #{'data': {'Reverting': {'RevertMergeCommit': {'id_1': {'user': "Mehmet Kaan Özkan"}, 'id_2': {'user': "Anıl Güvenç"}}}}}

        for errorObject in errorObjects:
            errorInfos = {}

            errorInfos['message'] = errorObject.message
            errorInfos['count'] = 0
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

                #commit['author'] = error.commit.author
                #commit['committer'] = error.commit.committer
                commit['additions'] = error.commit.additions
                commit['deletions'] = error.commit.deletions
                commit['changes'] = error.commit.changes
                commit['sha'] = error.commit.sha
                commit['message'] = error.commit.message
                commit['date'] = error.commit.date

                errorDetails['commit'] = commit
                errorDetails['extra_info'] = error.extra_info
                errorDetails['is_warning'] = error.is_warning

                errorInfos[error.error_id] = errorDetails
                errorInfos['count'] += 1

            if (errorObject.category not in data):
                data[errorObject.category] = {}
            data[errorObject.category][errorObject.name] = errorInfos

        return data

    def display_chart(self, my_data):
        names = []
        values = []
        for category,categoryv in my_data.items():
            for errorType,errors in categoryv.items():
                #print(errorType,len(errors))
                names.append(errorType)
                values.append(len(errors))

        return get_plot(names, values)
    def config_to_dict(self,request):
        avg_commit_day = request.GET.get("avg_commit_day")
        workflow = request.GET.get("workflow")
        user_config = {'avg_commit_day': avg_commit_day}
        user_config['workflow'] = workflow
        return user_config


model = Model()
controller = Controller(model)


def home(request):
    data = {'state': False, 'error': False, 'repo_name': None}
    user_config = controller.config_to_dict(request)
    print(user_config)

    if request.method == "GET":
        repoName = request.GET.get("repo")
        data['repo_name'] = repoName

        #if DEBUG == False, generate a new error detection. Otherwise, use cached one.

        if (settings.DEBUG == False and (repoName == "GitCheckup/GitCheckup" or repoName == "GitCheckup/demo")):
        #if (settings.DEBUG == True and repoName == "GitCheckup/GitCheckup" or repoName == "GitCheckup/demo"):
            if (repoName == "GitCheckup/GitCheckup"):
                data = config.GitCheckup_Data
                data['chart'] = controller.display_chart(data['data'])
            if (repoName == "GitCheckup/demo"):
                data = config.Demo_Data
                data['chart'] = controller.display_chart(data['data'])
        elif (repoName != "" and repoName != None):
            errorDetections = controller.analyze_repo(repoName,user_config)

            if (errorDetections == None):
                data['error'] = True
                return render(request, 'GitCheckup/index.html', data)

            data['data'] = controller.errors_to_dict(errorDetections)
            data['state'] = True

            #print(data)
            data['chart'] = controller.display_chart(data['data'])
        else:
            data['repo_name'] = "GitCheckup/GitCheckup"

    return render(request, 'GitCheckup/index.html', data)

def showMessage(request):
    return HttpResponse("Analyzed.")
