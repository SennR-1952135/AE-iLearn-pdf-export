import requests

from lib.utils.EnvUtils import get_env_url
from lib.utils.Authenticator import Authenticator

def get_learningTracks_json(pageNumber: int = 1, pageSize: int = 50, owner: str = 'Own', bearer_token: str = None):
    """
    Parameters
    ----------
    owner: 'Own', 'School', 'Other'
      The owner(s) of the learning tracks you want to access, default is 'Own'.
    """
    if not bearer_token:
        bearer_token = Authenticator.get_instance().get_bearer_token()
    
    payload = {
        'LearningActivityTypes': [],
        'LearningMaterialOwners': [owner],
        'OrderBy': "Descending",
        'Page': pageNumber,
        'PageSize': pageSize,
        'PublicationStatus': [],
        'Q': [],
        'SkosGroups': [],
        'SortBy': "Date",
        'Tools': [],
        'Types': ["learningTrack"]
    }

    headers = {
        'Authorization': 'Bearer ' + bearer_token,
    }

    api_url = get_env_url() + '/api/learningmaterials/query'

    res = requests.post(api_url, headers=headers, json=payload)

    return res.json()['items']