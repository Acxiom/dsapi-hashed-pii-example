import hashlib

from acxDataProcessor.entities.PhoneEntity import PhoneEntity                # pylint: disable=import-error
from acxDataProcessor.entities.AddressEntity import AddressEntity            # pylint: disable=import-error
from acxDataProcessor.entities.NameEntity import NameEntity                  # pylint: disable=import-error
from acxDataProcessor.entities.EmailEntity import EmailEntity                # pylint: disable=import-error
from acxDataProcessor.utils.DsapiParams import DsapiParams                   # pylint: disable=import-error
from acxDataProcessor.utils.DsapiServiceUtils import DsapiServiceUtils       # pylint: disable=import-error

class HashedEntityProcessor:
    def __init__(self, dsapiHelper: DsapiServiceUtils):
        self.dsapiHelper = dsapiHelper
        print("Started Hash Processor")

    def checkInputInformation(self, nameEntity: NameEntity=None, addressEntity: AddressEntity=None, phoneEntity: PhoneEntity=None, emailEntity: EmailEntity=None):
        (nameValid, addressValid, emailValid, phoneValid) = False, False, False, False

        if nameEntity:
            if nameEntity.isEligibleForDsapi():
                nameValid = True

        if addressEntity:
            if addressEntity.isEligibleForDsapi():
                addressValid = True

        if phoneEntity:
            if phoneEntity.isEligibleForDsapi():
                phoneValid = True

        if emailEntity:
            if emailEntity.isEligibleForDsapi():
                emailValid = True

        return (nameValid, addressValid, emailValid, phoneValid)

    def hashInputEntityStringSHA1(self, inputString):
        hashedString = hashlib.sha1()
        hashedString.update(inputString.encode(encoding='UTF-8'))

        return hashedString.hexdigest()

    def constructHashOnPriorities(self, data, dataPrioritySteps):
        (nameValid, addressValid, emailValid, phoneValid) = self.checkInputInformation(data['nameEntity'], data['addressEntity'], \
                data['phoneEntity'], data['emailEntity'])
        
        for step in dataPrioritySteps:
            if step == 'name + email' and nameValid and emailValid:
                return (self.hashInputEntityStringSHA1(data['nameEntity'].getLowerFormattedName() + ' ' + data['emailEntity'].getLowerEmailAddress()), 'name + email')
            elif step == 'name + phone' and nameValid and phoneValid:
                return (self.hashInputEntityStringSHA1(data['nameEntity'].getLowerFormattedName() + ' ' + data['phoneEntity'].getPhone()), 'name + phone')
            elif step == 'name + address' and nameValid and addressValid:
                return (self.hashInputEntityStringSHA1(data['nameEntity'].getLowerFormattedName() + ' ' + data['addressEntity'].getLowerFormattedAddress()), 'name + address')
            elif step == 'email' and emailValid:
                return (self.hashInputEntityStringSHA1(data['emailEntity'].getLowerEmailAddress()), 'email')
            elif step == 'phone' and phoneValid:
                return (self.hashInputEntityStringSHA1(data['phoneEntity'].getPhone()), 'phone')
            elif step == 'address' and addressValid:
                return (self.hashInputEntityStringSHA1(data['emailEntity'].getLowerEmailAddress()), 'address')

        raise ValueError("No suitable data process was found for data object!")
                
        

    def processDataChunkThroughEnhancement(self, dataChunk: [], requestParams: DsapiParams, dataPrioritySteps: []):
        processedData = []
        thisRequest = requestParams

        for dataRecord in dataChunk:
            dataTrail = {}
            # Construct the has of the input data based on the priorities
            (dataHash, hashMethod) = self.constructHashOnPriorities(dataRecord, dataPrioritySteps)

            dataTrail['hash'] = dataHash
            dataTrail['method'] = hashMethod
            dataTrail['origData'] = dataRecord
            
            # These were used in the single-call version of the dev scripts for testing
            # Leaving them in just in case, can be removed if there's no further use case
            #thisResponse = self.dsapiHelper.getHashPersonEnhancementObject(dataHash, thisRequest)
            #dataTrail['response'] = thisResponse

            print("Calculated Hash: " + dataHash + ' using method ' + hashMethod)
            processedData.append(dataTrail)

        dataTrail = self.dsapiHelper.getBatchHashPersonEnhancements(processedData, thisRequest)

        return processedData
