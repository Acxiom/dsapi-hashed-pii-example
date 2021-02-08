from acxDataProcessor.entities.DsapiParams import DsapiParams       # pylint: disable=import-error

class DsapiRequest:
    def __init__(self, params: DsapiParams, uri: str, payload: [] = None):
        self.params = params
        self.uri = uri
        self.payload = payload