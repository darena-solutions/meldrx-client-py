#
# MeldRx Python Client
#

import requests
import base64

class MeldRxClient:
    def __init__(self, base_url, client_id, client_secret, token_url):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.access_token = None
        self.verify = False     # ERM: TODO: We want to remove this eventually, but not sure how to get the SSL working

    def authenticate(self, scope):
        # Get authorization credentials...
        creds = self.client_id + ':' + self.client_secret
        creds = base64.b64encode(creds.encode('utf-8')).decode('utf-8')
        authHeader = 'Basic ' + creds

        headers = {
            'Authorization': authHeader,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'grant_type': 'client_credentials',
            'scope': scope
        }

        response = requests.post(self.token_url, headers=headers, data=data, verify=self.verify)
        self.access_token = response.json()['access_token']

    # Get the FHIR metadata...
    def getMetadata(self):
        response = requests.get(self.base_url + '/metadata', { 'Content-Type': 'application/json' }, verify=self.verify)
        return response.json()

    # Read a FHIR resource...
    def readResource(self, resourceType, resourceId):
        response = requests.get(self.base_url + '/' + resourceType + '/' + resourceId, headers=self.__get_headers(), verify=self.verify)
        return response.json()

    # Search for a FHIR resource...
    def searchResource(self, resourceType, params):
        response = requests.get(self.base_url + '/' + resourceType, params, headers=self.__get_headers(), verify=self.verify)
        return response.json()

    # Create a FHIR resource...
    def createResource(self, resourceType, data):
        response = requests.post(self.base_url + '/' + resourceType, data, headers=self.__get_headers(), verify=self.verify)
        return response.json()

    # Update a FHIR resource...
    def updateResource(self, resourceType, resourceId, data):
        response = requests.put(self.base_url + '/' + resourceType + '/' + resourceId, data, headers=self.__get_headers(), verify=self.verify)
        return response.json()

    # Delete a FHIR resource...
    def deleteResource(self, resourceType, resourceId):
        response = requests.delete(self.base_url + '/' + resourceType + '/' + resourceId, headers=self.__get_headers(), verify=self.verify)
        return response.json()

    # Get headers needed for requests
    def __get_headers(self):
        return {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json'
        }
