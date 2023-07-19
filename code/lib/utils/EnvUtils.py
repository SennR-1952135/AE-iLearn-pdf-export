import os
from enum import Enum
from utils.extract_url_id import extract_url_id

# create the env enum
class EnvENUM(Enum):
    # create the enum members
    DEV = 'https://dev.i-learn.be'
    TEST = 'https://test.i-learn.be'
    PROD = 'https://myway.i-learn.be'

# export the env url by getting the env enum value form the env variable
def get_env_url():
    return EnvENUM[os.getenv('ENV')].value

class EnvAuthENUM(Enum):
    # create the enum members
    DEV = 'https://auth-dev.i-learn.be/oauth/token'
    TEST = 'https://auth-test.i-learn.be/oauth/token'
    PROD = 'https://auth.i-learn.be/oauth/token'

def get_env_auth_url() -> str:
    return EnvAuthENUM[os.getenv('ENV')].value

class EnvClientIdENUM(Enum):
    # create the enum members
    DEV = 'oO7V4v23QcUBDHBxYs1VV4c59nfLVjzC'
    TEST = 'K4v7c44HdUEHzM7SUXfxZ0qimEY8LJW0'
    PROD = 'cXUqcDXEFmEF0001sKsmiyBhEBNnMPq2'

def get_env_client_id() -> str:
    return EnvClientIdENUM[os.getenv('ENV')].value

def get_lt_api_url(lt_url) -> str:
    lt_url = get_env_url() + '/api/learningmaterials/' + extract_url_id(lt_url)
    return lt_url

def get_lt_api_url_from_id(lt_id) -> str:
    lt_url = get_env_url() + '/api/learningmaterials/' + lt_id
    return lt_url


