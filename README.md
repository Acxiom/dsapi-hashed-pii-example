# Acxiom DS-API Hash Enhancement Processor

This module is for taking a static data set of PII from a standard file layout, converting the PII from the data set into SHA1 hashes, and sending the hashed entities to Acxiom's DS-API endpoint for demographics enhancements. Upon completion of the enhancement process, the file is recreated with the initial layout intact and all of the gathered data elements appended to the end of the initial columns.

This python module is provided as a starting point for hashed data processing and is not maintained by any official Acxiom product teams. By using this, parties understand that Acxiom is not liable for any data charges that are not expected by using this module.

## Features

 - Ability to enhance PII without the need for file transfers to/from Acxiom
 - Configurable hash creation rules to determine how granular the data hash should be
 - Configurable bundle specifications based on bought data

 ## Installation

 - Clone the repository
 - Execute ```pip install -e .```

 ## Usage

 ## Pre-Installation

 - Work with Acxiom data specialists to set up a license and get client credentials and secret to use in the module configuration
 
 ## Runtime

 - Extract data according to the file layout specifications
 - Create a copy of the config-template.yaml as config-prd.yaml and insert any customizations
    - Client key/secrect
    - Input/output file locations
    - DS-API request bundles (data packages)
    - Data chunk sizes (Max 1000)
    - Confirm hash creation priority steps
 - Execute ```python ./acxDataProcessor/runAcxDsapi.py```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. A to do list will be maintained for any nice to haves from the default environment.