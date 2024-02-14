import unittest
from src.MeldRxClient import MeldRxClient
from config import BASE_URL, TOKEN_URL, CLIENT_ID, CLIENT_SECRET, SCOPE

class TestMeldRxClient(unittest.TestCase):
    def test_authenticate_linkedApp_epic(self):
        # Make sure we can get an access token...
        client = MeldRxClient(BASE_URL, CLIENT_ID, CLIENT_SECRET, TOKEN_URL)
        client.authenticate(SCOPE)
        self.assertIsNotNone(client.access_token)

    def test_searchResource_linkedApp_epic(self):
        # Authenticate...
        client = MeldRxClient(BASE_URL, CLIENT_ID, CLIENT_SECRET, TOKEN_URL)
        client.authenticate(SCOPE)

        # Search for the resource...
        searchPatients = client.searchResource("Patient", { '_id': 'eD.LxhDyX35TntF77l7etUA3' })
        self.assertIsNotNone(searchPatients)
        self.assertEqual(searchPatients['resourceType'], 'Bundle')

