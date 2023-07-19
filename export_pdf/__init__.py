from lib.main import process_single
import logging
import azure.functions as func

export_pdf_bp = func.Blueprint()

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

def export_pdf(url: str, bearer_token: str):
    file_path = process_single(url, bearer_token)
    return file_path

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = get_param(req, 'name')
    id = get_param(req, 'id')
    print(id)
    
    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )