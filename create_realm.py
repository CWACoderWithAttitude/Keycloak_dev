# create_realm.py
import requests
from pprint import pprint

class KeycloakAdmin:
    def __init__(self, keycloak_root, keycloak_admin, keycloak_admin_password):
        self.keycloak_root = keycloak_root
        self.keycloak_admin = keycloak_admin
        self.keycloak_admin_password = keycloak_admin_password
        self.access_token = self.get_token()

    def get_token(self):
        resp = requests.post(
            f"{self.keycloak_root}/realms/master/protocol/openid-connect/token",
            data={
                "client_id": "admin-cli",
                "username": self.keycloak_admin,
                "password": self.keycloak_admin_password,
                "grant_type": "password"
            }
        )
        resp.raise_for_status()
        data = resp.json()
        access_token = data["access_token"]
        print(f"{access_token[:20]}...{access_token[-20:]}")
        print(f"Expires in {data['expires_in']}s")
        return access_token

    def get_auth_header(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
        }

    def get_realm(self):
        auth_headers = self.get_auth_header()
        resp = requests.get(
            f"{self.keycloak_root}/admin/realms",
            headers=auth_headers
        )
        resp.raise_for_status()
        return resp.json()

    def create_realm(self, realm_name):
        resp = requests.post(
            f"{self.keycloak_root}/admin/realms",
            headers=self.get_auth_header(),
            json={
                "realm": realm_name,
                "enabled": True
            }
        )
        resp.raise_for_status()
        return resp.json()
    def _check_client_exists(self, realm_name:str="n/a", client_id:str="n/a"):
        resp = requests.get(
            f"{self.keycloak_root}/admin/realms/{realm_name}/clients",
            headers=self.get_auth_header(),
        )
        resp.raise_for_status()
        clients = resp.json()
        for client in clients:
            if client["clientId"] == client_id:
                return True
        return False

    def create_public_client(self, realm_name:str="n/a", client_id:str="n/a", client_id_secret:str="n/a"):
        check_client_exists = self._check_client_exists(realm_name, client_id)
        if not check_client_exists:
            client_settings = {
                "protocol": "openid-connect",
                "clientId": client_id,
                "secret": client_id_secret,
                "redirectUris": ["http://localhost:8000/callback"],  # Replace with your app's redirect URIs
                "enabled": True,
                "publicClient": True,
                "standardFlowEnabled": True,    # Enable Authorization Code Flow
                "serviceAccountsEnabled": False,
                "directAccessGrantsEnabled": True,  # Enable Direct Access Grants (Resource Owner Password Credentials)
                "attributes": {
                    "oauth2.device.authorization.grant.enabled": True,
                }
            }

            resp = requests.post(
                f"{self.keycloak_root}/admin/realms/{realm_name}/clients",
                json=client_settings,
                headers=self.get_auth_header(),
            )
            resp.raise_for_status()
            location = resp.headers["Location"]
            return resp.json()

# Example usage
my_realm_name="oidc_realm1"
my_client_name="oidc_client2"
if __name__ == "__main__":
    keycloak_admin = KeycloakAdmin(
        keycloak_root="http://192.168.178.153:8080",
        keycloak_admin="admin",
        keycloak_admin_password="admin"
    )
    # Uncomment the following lines to test the methods
    #pprint(keycloak_admin.get_realm())
    #pprint(keycloak_admin.create_realm(my_realm_name))
    public_client = keycloak_admin.create_public_client(my_realm_name, my_client_name)
    pprint(public_client)
