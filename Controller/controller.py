from github import Github


class Controller:
    def __init__(self, model, view, gui_view=None, gui_top=None):
        # Our GitHub token for accessing the GitHub API
        self.git_access = Github("bd0d1460b6fd6e9edc00926b1f6a2b9c8b8339f0")
        self.gui_view = gui_view
        self.gui_top = gui_top
        self.view = view
        self.model = model


    # Method for parsing the repository address from the user and returns an appropriate string to get the repo from GitHub API
    def get_repo_address(self,repo_url=None):

        # address = input()

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

    def welcome_user(self):
        self.view.display_welcome()

    def analyze_repo(self):
        # view.display_input_repoAddress()

        while True:
            try:
                repo_address = self.get_repo_address()
            except:
                self.view.display_error_repoAddress()
                continue

            try:
                repo = self.get_repository(repo_address)
                break
            except:
                self.view.display_error_repoMissing()

        self.view.display_analyzing(repo_address)
        irepo = self.model.get_repo(repo)

        errorDetections = self.model.analyze_errors(irepo)

        totalErrorCount = 0
        for errorDetection in errorDetections:
            totalErrorCount += len(errorDetection.errorList)

        self.view.display_errors(errorDetections, totalErrorCount)

    def start_gui(self):

        self.gui_view.mainloop()
        self.gui_analyze_repo()

    def gui_analyze_repo(self):
        #print(self.get_repo_address(self.gui_top.repo_url))
        try:
            repo_address = self.get_repo_address(self.gui_top.repo_url)
            print(self.get_repo_address(self.gui_top.repo_url))
        except:
            pass
        try:
            repo = self.get_repository(repo_address)
        except:
            pass

        irepo = self.model.get_repo(repo)

        errorDetections = self.model.analyze_errors(irepo)

        totalErrorCount = 0
        for errorDetection in errorDetections:
            totalErrorCount += len(errorDetection.errorList)

        #self.view.display_errors(errorDetections, totalErrorCount)
        self.gui_top.display_errors(errorDetections, totalErrorCount)


        pass


