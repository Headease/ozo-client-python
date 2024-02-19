import requests
from flask import current_app


class NutsService:
    def __init__(self):
        pass

    @staticmethod
    def get_base_url():
        return current_app.config.get('NUTS_BASE_URL')

    @staticmethod
    def get_target_did():
        return current_app.config.get('DID_DATA_SOURCE')

    def _create_did(self, user_id):
        url = f'{self.get_base_url()}/internal/vdr/v2/did'
        data = {
            'id': user_id
        }
        return requests.post(url, json=data).json()

    def get_or_create_did(self, user_id) -> dict:
        url = f'{self.get_base_url()}/iam/{user_id}/did.json'
        resp = requests.get(url)
        if resp.status_code != 200:
            return self._create_did(user_id)
        else:
            return resp.json()

    def initiate_oid4vci_issue(self, user_id, redirect_uri):
        """
        This call to the local nuts-node will initiate an oid4vci flow, as part of the flow,
        the current user needs to be authenticated by the issuer, hence, the nuts-node
        will respond with a 302 redirect status. Once the issuance to the local nuts-node is done,
        the user will be redirected to the redirect_uri
        :param user_id: the user id if the current user
        :param redirect_uri: the location to redirect to.
        :return: a redirect location for the current user agent.
        """
        did = self.get_or_create_did(user_id)
        url = f'{self.get_base_url()}/iam/{did["id"]}/start-oid4vci-issuance'
        issuer = "did:web:issuer.ozo.headease.nl"
        credential_type = 'OzoUserCredential'
        data = {
            'issuer': issuer,
            'redirectURL': redirect_uri,
            'authorizationDetails': [
                {
                    "type": "openid_credential",
                    "format": "jwt_vc",
                    "credential_definition": {
                        "@context": [
                            "https://www.w3.org/2018/credentials/v1",
                            "https://cibg.nl/2024/credentials/" + credential_type.lower()
                        ],
                        "type": [
                            "VerifiableCredential",
                            credential_type
                        ]
                    }
                }
            ],
        }
        resp = requests.post(url, json=data, allow_redirects=False)
        if resp.status_code == 302:
            return resp.headers.get('Location')

        raise Exception("Did not receive a redirect from the nuts-node")

    def get_access_token(self, user_id):
        """
        This method request the local nuts-node for an access_token to the target_did nuts-node.
        The local nuts-node will handle the request to the nuts-node of the target_did.

        This method should eventually be something like "get fhir data", because the
        access_token should not be exposed to the mobile app.
        :param user_id: the user id if the current user
        :return:
        """
        target_did = self.get_target_did()
        requester = self.get_or_create_did(user_id)
        url = f'{self.get_base_url()}/internal/auth/v2/{requester["id"]}/request-service-access-token'
        data = {
            'verifier': target_did,
            'scope': 'ozo'
        }
        resp = requests.post(url, json=data)
        if resp.status_code == 200 or resp.status_code == 412:
            return resp.json()
        else:
            raise ValueError(f"Unexpected status ({resp.status_code}) from the nuts node.")


nuts_service = NutsService()
