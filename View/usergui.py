from View.application import Application
import tkinter as tk
from View.homepage import Homepage

class GuiView():
    def __init__(self, event, application):
        self.application = application
        self.event = event
        self.application.display_frame(Homepage)

    def debug(self, string):
        print(string)

    def display_error_repoAddress(self):
        self.application.frame.Scrolledtext1.insert(tk.INSERT, "Could not read repository address, please enter a valid address.\n","general_error_tag")

    def display_error_repoMissing(self):
        self.application.frame.Scrolledtext1.insert(tk.INSERT, "Could not find a valid repository with this address. Please ensure there are no typos and the repository is public.\n","general_error_tag")

    def display_analyzing(self, repoName):
        self.application.frame.Scrolledtext1.insert(tk.INSERT, "Analyzing repo: %s ...\n" % repoName,"analyzing_repo_tag")

    def display_errors(self, errorDetections, totalErrorCount):
        self.application.frame.Scrolledtext1.insert(tk.INSERT, "Analysis complete.","analysis_complete_message_tag")
        self.application.frame.Scrolledtext1.insert(tk.INSERT, "\n", "blank_tag")
        self.application.frame.Scrolledtext1.insert(tk.INSERT, "Found %d errors or poor practices.\n" % totalErrorCount,"result_statistics_tag")
        self.application.frame.Scrolledtext1.insert(tk.INSERT, "\n", "blank_tag")

        for detection in errorDetections:
            #self.application.frame.Scrolledtext1.insert(tk.INSERT, "-------------------------------\n","seperator_tag")
            self.application.frame.Scrolledtext1.insert(tk.INSERT, "\n", "blank_tag")
            self.application.frame.Scrolledtext1.insert(tk.INSERT, "Found %d issues of type %s of category %s:\n\n" % (len(detection.errorList), detection.name, detection.category),"category_of_error_tag")


            for error in detection.errorList:
                self.application.frame.Scrolledtext1.insert(tk.INSERT, "User: %s (@%s) made an error%s at: %s on commit sha: %s with message: %s\n" % (error.user.name, error.user.username, error.extra_info, error.commit.date, error.commit.sha, error.commit.message),"user_error_report_tag")

        self.application.frame.Scrolledtext1.see(tk.END)
