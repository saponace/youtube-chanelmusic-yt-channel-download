class FileMatchesNoRegexError(Exception):
    def __init__(self, message):
        self.message = message
        print("Error: " + message)
