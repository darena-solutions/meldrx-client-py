import requests
import base64

class FHIRClient:
    def __init__(self, base_url, access_token, access_token_type):
        self.base_url = base_url
        self.access_token = access_token
        self.access_token_type = access_token_type

    # Initialize the FHIRClient with a Bearer token...
    @staticmethod
    def for_bearer_token(accessToken):
        return FHIRClient(None, accessToken, "Bearer")

    # Initialize the FHIRClient for Basic Auth...
    @staticmethod
    def for_basic_auth(base_url, user, pwd):
        # Create the access token by combining user/pwd...
        access_token = user + ':' + pwd
        access_token = base64.b64encode(access_token.encode('utf-8')).decode('utf-8')
        return FHIRClient(base_url, access_token, "Basic")

    # Read a FHIR resource...
    def readResource(self, resourceType, resourceId):
        url = self.__construct_fhir_url(resourceType, resourceId)
        response = requests.get(url, headers=self.__get_headers())
        return response.json()

    # Search for a FHIR resource...
    def searchResource(self, resourceType, params):
        url = self.__construct_fhir_url(resourceType)
        response = requests.get(url, params, headers=self.__get_headers())
        return response.json()

    # Create a FHIR resource...
    def createResource(self, resourceType, data):
        url = self.__construct_fhir_url(resourceType)
        response = requests.post(url, data, headers=self.__get_headers())
        return response.json()

    # Update a FHIR resource...
    def updateResource(self, resourceType, resourceId, data):
        url = self.__construct_fhir_url(resourceType, resourceId)
        response = requests.put(url, data, headers=self.__get_headers())
        return response.json()

    # Delete a FHIR resource...
    def deleteResource(self, resourceType, resourceId):
        url = self.__construct_fhir_url(resourceType, resourceId)
        response = requests.delete(url, headers=self.__get_headers())
        return response.json()

    # Get the authorization header for this instance...
    def __get_auth_header_value(self):
        return self.access_token_type + ' ' + self.access_token,

    # Get headers needed for requests
    def __get_headers(self):
        return {
            'Authorization': self.__get_auth_header_value(),
            'Content-Type': 'application/json'
        }

    # Construct the FHIR URL...
    def __construct_fhir_url(self, resourceType, resourceId = None, historyVersion = None):
        url = self.base_url + '/' + resourceType
        if resourceId:
            url += '/' + resourceId

        if historyVersion:
            url += '/_history/' + historyVersion

        return url