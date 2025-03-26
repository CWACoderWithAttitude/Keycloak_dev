from keycloak import KeycloakAdmin

class OIDCSetup:
    # Keycloak server configuration
    KEYCLOAK_SERVER_URL = "http://localhost:8080/auth/"  # Replace with your Keycloak server URL
    KEYCLOAK_ADMIN_USERNAME = "admin"  # Replace with your Keycloak admin username
    KEYCLOAK_ADMIN_PASSWORD = "admin"  # Replace with your Keycloak admin password
    KEYCLOAK_REALM = "myrealm"  # Replace with your desired realm name
    OIDC_CLIENT_ID = "myclient"  # Replace with your desired client ID
    OIDC_CLIENT_SECRET = "myclientsecret"  # Replace with your desired client secret
    REDIRECT_URIS = ["http://localhost:8000/callback"]  # Replace with your app's redirect URIs

    def init_keycloak_admin(self):
        # Initialize Keycloak Admin client
        keycloak_admin = KeycloakAdmin(
            server_url=self.KEYCLOAK_SERVER_URL,
            username=self.KEYCLOAK_ADMIN_USERNAME,
            password=self.KEYCLOAK_ADMIN_PASSWORD,
            realm_name="master",  # Use the master realm for admin operations
            verify=True,
        )
        return keycloak_admin

    # Initialize Keycloak Admin client
    
    def create_realm(self, realm_name):
        
    # Step 1: Create a new realm (if it doesn't already exist)
    realms = keycloak_admin.get_realms()
    if not any(realm["realm"] == KEYCLOAK_REALM for realm in realms):
        keycloak_admin.create_realm(
            {
                "realm": KEYCLOAK_REALM,
                "enabled": True,
            }
        )
        print(f"Realm '{KEYCLOAK_REALM}' created successfully!")

    # Switch to the new realm
    keycloak_admin.realm_name = KEYCLOAK_REALM

    # Step 2: Create a new OIDC client
    clients = keycloak_admin.get_clients()
    if not any(client["clientId"] == OIDC_CLIENT_ID for client in clients):
        keycloak_admin.create_client(
            {
                "clientId": OIDC_CLIENT_ID,
                "secret": OIDC_CLIENT_SECRET,
                "enabled": True,
                "redirectUris": REDIRECT_URIS,
                "protocol": "openid-connect",
                "publicClient": False,  # Set to False for confidential clients
                "standardFlowEnabled": True,  # Enable Authorization Code Flow
                "implicitFlowEnabled": False,
                "directAccessGrantsEnabled": True,  # Enable Direct Access Grants (Resource Owner Password Credentials)
            }
        )
        print(f"OIDC client '{OIDC_CLIENT_ID}' created successfully!")

    # Step 3: Add roles (optional)
    roles = keycloak_admin.get_roles()
    if not any(role["name"] == "user" for role in roles):
        keycloak_admin.create_role({"name": "user"})
        print("Role 'user' created successfully!")

    # Step 4: Add users (optional)
    users = keycloak_admin.get_users()
    if not any(user["username"] == "testuser" for user in users):
        keycloak_admin.create_user(
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "enabled": True,
                "credentials": [{"type": "password", "value": "testpassword", "temporary": False}],
            }
        )
        print("User 'testuser' created successfully!")

    print("Keycloak OIDC configuration completed!")