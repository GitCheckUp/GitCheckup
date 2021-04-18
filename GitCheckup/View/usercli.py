class CommandLineView:
    def __init__(self):
        pass

    def display(self, string):
        print(string)

    def display_welcome(self):
        print("Welcome to GitCheckup!")

    def display_input_repoAddress(self):
        print("Please enter repository address: ")

    def display_error_repoAddress(self):
        print("Could not read repository address, please enter a valid address.")

    def display_error_repoMissing(self):
        print("Could not find a valid repository with this address. Please ensure there are no typos and the repository is public.")

    def display_analyzing(self, repoName):
        print("Analyzing repo: %s ...\n" % repoName)

    def display_errors(self, errorDetections, totalErrorCount):
        print("Analysis complete.")
        print("Found %d errors or poor practices." % totalErrorCount)

        for detection in errorDetections:
            print("-------------------------------")
            print("Found %d issues of type %s of category %s:\n" % (len(detection.errorList), detection.name, detection.category))

            for error in detection.errorList:
                print("User: %s made an error%s at: %s on commit sha: %s with message: %s" % (error.user.name, error.extra_info, error.commit.date, error.commit.sha, error.commit.message))


