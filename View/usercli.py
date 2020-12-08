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

