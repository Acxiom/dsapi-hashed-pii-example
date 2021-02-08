class EmailEntity:
    def __init__(self, emailAddress):
        self.emailAddress = emailAddress

    def isEligibleForDsapi(self):
        if not self.emailAddress:
            return False
        else:
            return True

    def getEmailAddress(self):
        return self.emailAddress

    def getLowerEmailAddress(self):
        return self.emailAddress.lower()