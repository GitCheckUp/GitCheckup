from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from .utils import get_bar_plot, get_pie_plot
import sys
import time

sys.path.append(".")

from GitCheckup.Model.model import Model
from GitCheckup.Model import iauthor
from GitCheckup.Model.config import config
from github import Github

class Controller():
    def __init__(self, model):
        # Our GitHub token for accessing the GitHub API
        self.git_access = [Github("bd0d1460b6fd6e9edc00926b1f6a2b9c8b8339f0"), Github("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"), Github("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")]
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
        for token in self.git_access:
            try:
                return token.get_repo(repo_address)
            except:
                print("failed token:", token)
                pass
        return None

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
        self.model.create_irepo(repo)

        errorDetections = self.model.analyze_errors(model.irepo, user_config)

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

    def get_error_detection_counts(self):
        names = []
        values = []
        for errorObject in self.model.errorDetections:
            names.append(errorObject.name)
            values.append(len(errorObject.errorList))

        return (values, names)

    def get_user_errors(self):
        users = {}
        for author in iauthor.authors.values():
            if (author.name != ""):
                users[author.name] = 0

        for errorDetectionObject in model.errorDetections:
            for error in errorDetectionObject.errorList:
                if error.user and error.user.name in users:
                    users[error.user.name] += 1

        return (users.values(), users.keys())

    def get_user_commits(self):
        users = {}
        for author in iauthor.authors.values():
            if (author.name != ""):
                users[author.name] = 0

        for commit in model.irepo.commitList:
            if commit.author and commit.author.name in users:
                users[commit.author.name] += 1

        return (users.values(), users.keys())

    def display_visual(self, my_data):
        visual_dict = {}
        print(*self.get_error_detection_counts())
        visual_dict['chart'] = get_bar_plot(*self.get_error_detection_counts(), "Count of each error/poor practice type", "Total errors/poor practices: " + str(len([subitem for sublist in [errorDetectionObject.errorList for errorDetectionObject in model.errorDetections] for subitem in sublist])))
        visual_dict['pie'] = get_pie_plot(*self.get_error_detection_counts(), "Pie chart for the percentage of each error/poor practice")
        visual_dict['pie_user-errors'] = get_pie_plot(*self.get_user_errors(), "Pie chart for errors/poor practices per user")
        visual_dict['pie_user-commits'] = get_pie_plot(*self.get_user_commits(), "Pie chart for commits per user", "Total commits: " + str(len(model.irepo.commitList)))

        return visual_dict

    def config_to_dict(self,request):
        avg_commit_day = request.GET.get("avg_commit_day")
        workflow = request.GET.get("workflow")
        max_file = request.GET.get("max_file")
        user_config = {'avg_commit_day': avg_commit_day}
        user_config['workflow'] = workflow
        user_config['max_file'] = max_file
        return user_config


model = Model()
controller = Controller(model)


def home(request):
    data = {'state': False, 'error': False, 'repo_name': None}
    user_config = controller.config_to_dict(request)

    if request.method == "GET":
        repoName = request.GET.get("repo")
        data['repo_name'] = repoName

        #if DEBUG == False, generate a new error detection. Otherwise, use cached one.

        if (settings.DEBUG == False and (repoName == "GitCheckup/GitCheckup" or repoName == "GitCheckup/demo")):
        #if (settings.DEBUG == True and repoName == "GitCheckup/GitCheckup" or repoName == "GitCheckup/demo"):
            if (repoName == "GitCheckup/GitCheckup"):
                data = config.GitCheckup_Data
                data['visual'] = controller.display_visual(data['data'])
            if (repoName == "GitCheckup/demo"):
                data = config.Demo_Data
                data['visual'] = controller.display_visual(data['data'])
        elif (repoName != "" and repoName != None):
            errorDetections = controller.analyze_repo(repoName,user_config)
            model.errorDetections = errorDetections

            if (errorDetections == None):
                data['error'] = True
                return render(request, 'GitCheckup/index.html', data)

            data['data'] = controller.errors_to_dict(errorDetections)
            data['state'] = True

            #print(data)
            data['visual'] = controller.display_visual(data['data'])
        else:
            data['repo_name'] = "GitCheckup/GitCheckup"

    return render(request, 'GitCheckup/index.html', data)

def showMessage(request):
    return HttpResponse("Analyzed.")
