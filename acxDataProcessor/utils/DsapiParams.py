class DsapiParams:
    def __init__(self, limit=1, bundles = [], role=None, tenant=None, format = 'json'):
        self.limit = limit
        self.bundles = bundles
        self.role = role
        self.tenant = tenant
        self.format = format

    def formatForRequest(self):
        formattedString = '?'
        numParams = 0
        if self.limit:
            formattedString += 'limit=' + str(self.limit)
            numParams += 1
        
        if self.bundles:
            if numParams >= 1:
                formattedString += '&'

            formattedString += 'bundle=' + ','.join(self.bundles)
        
        if self.role:
            if numParams >= 1:
                formattedString += '&'

            formattedString += 'role=' + self.role

        if self.tenant:
            if numParams >= 1:
                formattedString += '&'

            formattedString += 'tenant=' + self.tenant

        if self.format:
            if numParams >= 1:
                formattedString += '&'

            formattedString += 'format=' + self.format

        return formattedString