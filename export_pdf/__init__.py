import logging
import azure.functions as func
from .utils import get_param


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = get_param(req, 'name')
    bearer_token = req.headers.get('Authorization')
    id = get_param(req, 'id')
    logging.info('id: ' + id)
    logging.info('bearer_token: ' + bearer_token)

    return func.HttpResponse(
        f"Hello, {name}. id is {id}. bearer_token is {bearer_token}. This HTTP triggered function executed successfully.",
        status_code=200
    )