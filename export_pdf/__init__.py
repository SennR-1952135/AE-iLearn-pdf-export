import logging
import azure.functions as func
from .utils import get_param


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    bearer_token = req.headers.get('Authorization')
    id = get_param(req, 'id')
    logging.info('id: ' + id)
    logging.info('bearer_token: ' + bearer_token)

    if not id:
        return func.HttpResponse(
            "Please pass a learning-track-id as a parameter on the query string",
            status_code=400
        )
    
    if not bearer_token:
        return func.HttpResponse(
            "Unauthorized: Please pass a bearer token in the Authorization header",
            status_code=401
        )
    
    try:
      return func.HttpResponse(
          f"Id is {id}. bearer_token is {bearer_token}. This HTTP triggered function executed successfully.",
          status_code=200
      )
    except Exception as e:
      return func.HttpResponse(
          f"Error: {e}",
          status_code=500
      )
        
