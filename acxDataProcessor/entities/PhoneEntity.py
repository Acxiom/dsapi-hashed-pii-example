class PhoneEntity:
    def __init__(self, phone):
        self.phone = phone

    def isEligibleForDsapi(self):
        if not self.phone:
            return False
        else:
            return True

    def getPhone(self):
        if self.isEligibleForDsapi():
            return self.phone
        else:
            raise ValueError("Phone number was not valid.")