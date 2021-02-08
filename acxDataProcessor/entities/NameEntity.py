class NameEntity:
    def __init__(self, firstName, middleName, lastName, generationalSuffix):
        self.firstName = firstName
        self.middleName = middleName
        self.lastName = lastName
        self.generationalSuffix = generationalSuffix

    #Making sure that we have at least a first + last name
    def isEligibleForDsapi(self):
        if not self.firstName and not self.lastName:
            return False
        
        return True

    def getFormattedName(self):
        if self.isEligibleForDsapi:
            finalName = ''
            
            if self.firstName:
                finalName = self.firstName
            
            if self.middleName:
                finalName += ' ' + self.middleName

            if self.lastName:
                finalName += ' ' + self.lastName

            if self.generationalSuffix:
                finalName += ' ' + self.generationalSuffix

            return finalName.translate({ord(i): None for i in '.'})
        else:
            raise ValueError("Name isn't eligible for return. Must include at least first and last name.")

    def getLowerFormattedName(self):
            return self.getFormattedName().lower()