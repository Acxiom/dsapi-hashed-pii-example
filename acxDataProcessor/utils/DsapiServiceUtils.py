import requests, datetime, time, json

import acxDataProcessor.utils.DsapiParams as DSAPI_PARAMS   # pylint: disable=import-error

class DsapiServiceUtils:
    def getToken(self):        
        response = requests.post(self.stsUrl, data=self.payload)
        if response.status_code == 200:
            data = json.loads(response.text)
            self.accessToken = data['access_token']
            self.expiresIn = data['expires_in'] #in seconds
            self.getExpirationTime()
            print("Fetched token that expires in " + str(self.expiresIn) + " seconds.")
            return (self.accessToken, self.expiresIn)
        else:
            print('Failed to obtain access token, status code ' + str(response.status_code))
            return ('', '0')

    # This just calculates the expiration time for future checks. It's split out to clean the get token code up
    def getExpirationTime(self):
        bufferTime = 60
        currentTime = datetime.datetime.now()
        unixTimestamp = time.mktime(currentTime.timetuple())
        self.expiresAt = unixTimestamp + int(self.expiresIn) - bufferTime
                
    # Determines if the token has expired and requires a new one
    # TODO: Build in more buffer time from the above calculation?
    def isTokenExpiring(self):
        currentTime = datetime.datetime.now()
        unixTimestamp = time.mktime(currentTime.timetuple())
        
        if unixTimestamp >= self.expiresAt:
            return True
        
        return False

    # Runs a GET call to the specified URI for the dsapiUri from the config file
    # This requires that the URI be passed every time
    def get(self, uri, payload: DSAPI_PARAMS=None):
        if(self.isTokenExpiring()):
            self.getToken()

        headers = {
            "Authorization": "Bearer " + self.accessToken, #This header is required
            "Accept": "application/json" #this can be application/xml or text/html
        }
        
        response = requests.get(self.dsapiUri + uri + payload.formatForRequest(), headers=headers)
        return response

    def post(self, uri, params: DSAPI_PARAMS, body: []):
        if(self.isTokenExpiring()):
            self.getToken()

        headers = {
            "Authorization": "Bearer " + self.accessToken, #This header is required
            "Accept": "application/json" #this can be application/xml or text/html
        }

        response = requests.post(self.dsapiUri + uri + '?format=json', json=body, headers = headers)
        print(response.text)

        return json.loads(response.text)

    def getBatchHashPersonEnhancements(self, dataTrail: {}, requestParams: DSAPI_PARAMS):
        endpoint = '/batch/lookup'
        dataEndpointToken = '/people/sha1/'
        payload = []

        for record in dataTrail:
            payload.append(dataEndpointToken + record['hash'] + '?bundle=' + ','.join(requestParams.bundles))
            
        response = self.post(endpoint, requestParams, payload)

        responseNum = 0
        for record in dataTrail:
            record['response'] = response[responseNum]
            responseNum += 1

        return dataTrail


    def getHashPersonEnhancementObject(self, hashedData: str, params: DSAPI_PARAMS):
        endpoint = '/people/sha1/' + hashedData
        response = self.get(endpoint, params)
        return response

    def __init__(self, apiKey, apiSecret, tokenEndpoint, dsapiUri):
        self.dsapiUri = dsapiUri
        self.stsUrl = tokenEndpoint
        self.payload= {'client_id' : apiKey,'client_secret':apiSecret, 'grant_type':'client_credentials'}
        self.getToken()
