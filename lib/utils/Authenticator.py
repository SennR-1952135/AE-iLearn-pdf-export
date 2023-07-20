import requests
from lib.utils.EnvUtils import get_env_auth_url, get_env_client_id

class Authenticator:
    _instance = None

    @staticmethod
    def get_instance():
        if not Authenticator._instance:
            Authenticator()
        return Authenticator._instance

    def __init__(self, username: str, password: str) -> None:
        if Authenticator._instance:
            raise Exception("Authenticator instance already exists. Use get_instance() to retrieve it.")
        self.username = username
        self.password = password
        self.bearer_token = None
        Authenticator._instance = self

    def get_bearer_token(self) -> str:
        if not self.bearer_token:
            # Logic to obtain the bearer token using self.username and self.password
            self.bearer_token = self._authenticate()
        return self.bearer_token

    def _authenticate(self) -> str:
        client_id = get_env_client_id()
        url = get_env_auth_url()
        
        response = requests.post(
                url,
                json={
                    "grant_type": "password",
                    "client_id": client_id,
                    "username": self.username,
                    "password": self.password,
                    "scope": "openid profile email",
                }
            )
        if response.status_code != 200:
            raise Exception("Authentication failed")

        return response.json()['access_token']
    
    def authenticate_user(self, username, password) -> str:
        """Authenticate user with username and password, instantiates Singleton Authenticator class

        Returns
        -------
        str: bearer_token
        """
        if username and password:
          self.username = username
          self.password = password
          
        elif not self.username and not self.password:
            raise Exception("No username and password provided")
            print("ERROR: No username and password provided")
            # bearer_token = args.bearer_token if args.bearer_token else os.getenv("BEARER_TOKEN")
        
        bearer_token = self.get_bearer_token() # Instantiate Authenticator class and call get_bearer_token method
        return bearer_token
    

        
