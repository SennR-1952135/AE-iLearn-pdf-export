from lib.main import process_single
from lib.utils.EnvUtils import get_lt_api_url_from_id
import azure.functions as func

def get_param(req: func.HttpRequest, param_name: str):
    param = req.params.get(param_name)
    if not param:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            param = req_body.get(param_name)
    return param

def export_pdf(id: str, bearer_token: str):
    api_url = get_lt_api_url_from_id(id)
    file_path = process_single(api_url, bearer_token)
    return file_path