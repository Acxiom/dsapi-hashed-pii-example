class AddressEntity:
    def __init__(self, primaryNumber, preDirectional, street, streetSuffix, postDirectional, \
        unitDesignator, secondaryNumber, city, state, zipCode, zipExtension):
        self.primaryNumber = primaryNumber
        self.preDirectional = preDirectional
        self.street = street
        self.streetSuffix = streetSuffix
        self.postDirectional = postDirectional
        self.unitDesignator = unitDesignator
        self.secondaryNumber = secondaryNumber
        self.city = city
        self.state = state
        self.zipCode = zipCode
        self.zipExtension = zipExtension

    def isEligibleForDsapi(self):
        if not self.primaryNumber or not self.street or not self.city or not self.state or not self.zipCode:
            return False
        else:
            return True

    def getFormattedAddress(self):
        finalAddress = ''

        if self.isEligibleForDsapi():
            if self.primaryNumber:
                finalAddress += self.primaryNumber
            if self.preDirectional:
                finalAddress += ' ' + self.preDirectional
            if self.street:
                finalAddress += ' ' + self.street
            if self.streetSuffix:
                finalAddress += ' ' + self.streetSuffix
            if self.postDirectional:
                finalAddress += ' ' + self.postDirectional
            if self.unitDesignator:
                finalAddress += ' ' + self.unitDesignator
            if self.secondaryNumber:
                finalAddress += ' ' + self.secondaryNumber
            if self.city:
                finalAddress += ' ' + self.city
            if self.state:
                finalAddress += ' ' + self.state
            if self.zipCode:
                finalAddress += ' ' + self.zipCode
            # DS-API doesn't support using ZIP extension as part of the hash.
            # Use the function getFormattedAddressWithZip4 to get string with extension
            #if self.zipExtension:
            #    finalAddress += ' ' + self.zipExtension
        else:
            raise ValueError("Address does not include at least the following: primary number, street, city, state, and/or postal code.")

        return finalAddress.translate({ord(i): None for i in '.'})

    def getFormattedAddressWithZip4(self):
        finalAddress = ''

        if self.isEligibleForDsapi():
            if self.primaryNumber:
                finalAddress += self.primaryNumber
            if self.preDirectional:
                finalAddress += ' ' + self.preDirectional
            if self.street:
                finalAddress += ' ' + self.street
            if self.streetSuffix:
                finalAddress += ' ' + self.streetSuffix
            if self.postDirectional:
                finalAddress += ' ' + self.postDirectional
            if self.unitDesignator:
                finalAddress += ' ' + self.unitDesignator
            if self.secondaryNumber:
                finalAddress += ' ' + self.secondaryNumber
            if self.city:
                finalAddress += ' ' + self.city
            if self.state:
                finalAddress += ' ' + self.state
            if self.zipCode:
                finalAddress += ' ' + self.zipCode
            if self.zipExtension:
                finalAddress += ' ' + self.zipExtension
        else:
            raise ValueError("Address does not include at least the following: primary number, street, city, state, and/or postal code.")

        return finalAddress
    
    def getLowerFormattedAddress(self):
        return self.getFormattedAddress().lower()
