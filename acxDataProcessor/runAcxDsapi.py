import yaml, os, hashlib
from acxDataProcessor.utils.DsapiServiceUtils import DsapiServiceUtils  # pylint: disable=import-error
from acxDataProcessor.utils.DsapiFileUtils import DsapiFileUtils        # pylint: disable=import-error
from acxDataProcessor.utils.DsapiParams import DsapiParams              # pylint: disable=import-error

props = []

module_dir = os.path.dirname(os.path.realpath(__file__))

print("Current module dir is " + module_dir)

with open(os.path.join(module_dir, 'config-prd.yaml')) as file:
    props = yaml.load(file, Loader=yaml.FullLoader)

#Instantiate the DS-API helper
dsapiUtil = DsapiServiceUtils(props['acxiomKey'], props['acxiomSecret'], props['tokenEndpoint'], props['dsapiUri'])

# Initiating the file processor that will start the work
thisFile = DsapiFileUtils(props['inFileLocation'], props['outFileLocation'], fileHeaderRows = props['fileHeaderRows'], chunkSize = props['chunkProcessingSize'])

# Setting the parameters for the request since they're located in the configuration file
requestParams = DsapiParams(props['limit'], props['dsapiRequestBundles'], props['role'], props['tenant'], props['format'])

# Starting the actual work
thisFile.processFileThroughAppend(props['lookupType'], requestParams, props['dataPrioritySteps'], dsapiUtil)
