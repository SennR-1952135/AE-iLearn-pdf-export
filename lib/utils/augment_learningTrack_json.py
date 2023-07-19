import json
import requests
from lib.utils.EnvUtils import get_env_url
from lib.utils.Authenticator import Authenticator

def augment_learningTrack_json(json: dict) -> dict:
    """Augments the learning track json with fields that need to be
    requested via the api or added manually"""
    _transform_empty_p_tags_to_br_tags(json)
    _transform_childStep_keys(json)
    _transform_learningMaterialIconURL(json)
    _add_learningMaterial_info(json)
    return json

def _transform_learningMaterialIconURL(json: dict) -> None:
    """transforms url to full url instead of relative url"""
    for step in json['steps']:
        if 'learningMaterialIcon' in step:
            step['learningMaterialIcon'] = get_env_url() + "/" + step['learningMaterialIcon']

def _add_learningMaterial_info(json: dict) -> None:
    """adds the learning material info to the step"""
    for step in json['steps']:
        if 'learningMaterial' in step:
            learningMaterial_info = _get_learningMaterial_info(step['learningMaterial'])
            if not learningMaterial_info: continue
            step['learningMaterialURL'] = learningMaterial_info['urlOfActivity']
        
def _get_learningMaterial_info(learningMaterialId: str) -> dict:
    """gets the learning material info from the api"""
    try:
      res = requests.get(get_env_url() + "/api/learningmaterials/" + learningMaterialId, headers={'Authorization': 'Bearer ' + Authenticator.get_instance().get_bearer_token()})
      return res.json()
    except:
      print("ERROR: Could not get learning material info for learning material with id: " + learningMaterialId)
      return None


def _transform_childStep_keys(obj:json) -> None:
    """transforms childStepkeys to childStepId"""
    if isinstance(obj, dict):
        if 'childStep' in obj:
            obj['childStepId'] = obj['childStep']
            del obj['childStep']
        for key, value in obj.items():
            _transform_childStep_keys(value)
    elif isinstance(obj, list):
        for item in obj:
            _transform_childStep_keys(item)

def _transform_empty_p_tags_to_br_tags(json: dict) -> None:
    """adds br tags to p tags, needed for the html (platypus reportlab) renderer"""
    if isinstance(json, dict):
        for key, value in json.items():
            if isinstance(value, str):
                json[key] = value.replace('<p></p>', '<br/>')
            else:
                _transform_empty_p_tags_to_br_tags(value)
    elif isinstance(json, list):
        for item in json:
            _transform_empty_p_tags_to_br_tags(item)
    