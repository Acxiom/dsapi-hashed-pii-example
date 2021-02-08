from acxDataProcessor.entities.AddressEntity import AddressEntity                   # pylint: disable=import-error
from acxDataProcessor.entities.NameEntity import NameEntity                         # pylint: disable=import-error
from acxDataProcessor.entities.EmailEntity import EmailEntity                       # pylint: disable=import-error
from acxDataProcessor.entities.PhoneEntity import PhoneEntity                       # pylint: disable=import-error
from acxDataProcessor.utils.OutputProcessor import OutputProcessor                  # pylint: disable=import-error
from acxDataProcessor.utils.HashedEntityProcessor import HashedEntityProcessor      # pylint: disable=import-error
from acxDataProcessor.utils.DsapiParams import DsapiParams                          # pylint: disable=import-error
from acxDataProcessor.utils.DsapiServiceUtils import DsapiServiceUtils              # pylint: disable=import-error
from acxDataProcessor.utils.OutputProcessor import OutputProcessor                  # pylint: disable=import-error

import csv

class DsapiFileUtils:
    def __init__(self, infile, outfile, fileHeaderRows = 0, chunkSize = 5):
        self.infile = infile
        self.outfile = outfile
        self.chunkSize = chunkSize
        self.fileHeaderRows = fileHeaderRows
        self.workDb = OutputProcessor()

    def getDataChunksForProcess(self, csvReader):
        dataChunk = []
        
        for lineNumber, data in enumerate(csvReader):
#            if lineNumber + 1 <= self.fileHeaderRows:
#                continue
#            else:
            dataChunk.append(data)

            if len(dataChunk) % self.chunkSize == 0 and lineNumber > 0:
                print("Returning chunk of size " + str(len(dataChunk)))
                yield dataChunk
                del dataChunk[:]
            
        yield dataChunk

    def mapStandardFileToEntities(self, dataRow):
        thisAddressEntity = None
        thisEmailEntity = None
        thisNameEntity = None
        thisPhoneEntity = None
        
        thisNameEntity = NameEntity(dataRow['firstName'], dataRow['middleName'], dataRow['lastName'], dataRow['generationalSuffix'])
        thisAddressEntity = AddressEntity(dataRow['primaryNumber'], dataRow['preDirectional'], dataRow['street'], dataRow['streetSuffix'], \
            dataRow['postDirectional'], dataRow['unitDesignator'], dataRow['secondaryNumber'], dataRow['city'], dataRow['state'], dataRow['zipCode'], dataRow['zipExtension'])
        thisEmailEntity = EmailEntity(dataRow['email'])
        thisPhoneEntity = PhoneEntity(dataRow['phone'])

        return thisNameEntity, thisAddressEntity, thisEmailEntity, thisPhoneEntity


    def processFileThroughAppend(self, lookupType, requestParams: DsapiParams, dataPrioritySteps: [], dsapiHelper: DsapiServiceUtils):
        reader = csv.DictReader(open(self.infile, 'r'))
        hashedEntityProcessing = HashedEntityProcessor(dsapiHelper)

        totalProcessChunks = 0
        for chunk in self.getDataChunksForProcess(reader):
            mappedData = []
            for dataRow in chunk:
                thisMappedRow = {}
                thisMappedRow['origDataRow'] = dataRow
                (thisMappedRow['nameEntity'], thisMappedRow['addressEntity'], thisMappedRow['emailEntity'], thisMappedRow['phoneEntity']) = self.mapStandardFileToEntities(dataRow)
                mappedData.append(thisMappedRow)

            # Diverging to do the correct lookup for the specified lookup type
            if lookupType == 'sha1':
                processedData = hashedEntityProcessing.processDataChunkThroughEnhancement(mappedData, requestParams, dataPrioritySteps)
                self.workDb.processOutputIntoDb(processedData)
                
                print("stop here")
            elif lookupType == 'file':
                print("This will eventuall just output a file of hashes for direct sends.")

            totalProcessChunks += 1
        
        
        self.workDb.outputAllDbRowsToFile(self.outfile)