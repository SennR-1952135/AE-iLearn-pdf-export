import logging, os
import azure.functions as func
from .utils import get_param
from lib.main import process_single_azure
from lib.utils.EnvUtils import get_lt_api_url_from_id


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    bearer_token = req.headers.get('Authorization')
    id = get_param(req, 'id')
    # logging.info('id: ' + id)
    # logging.info('bearer_token: ' + bearer_token)

    if not id:
        return func.HttpResponse(
            "Please pass a learning-track-id as a parameter (ex. &id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx) on the query string",
            status_code=400
        )
    
    if not bearer_token:
        return func.HttpResponse(
            "Unauthorized: Please pass a bearer token in the Authorization header",
            status_code=401
        )
    
    try:
      bearer_token = bearer_token.replace('Bearer ', '')
      api_url = get_lt_api_url_from_id(id)
      file_stream = process_single_azure(api_url, bearer_token)

      # return func.HttpResponse(
      #     f"Id is {id}. bearer_token is {bearer_token}. root_path is {root_path}. root_path2 is {root_path2}. Filepath is {file_path}. This HTTP triggered function executed successfully.",
      #     status_code=200
      # )
    except Exception as e:
      return func.HttpResponse(
          f"Error exporting pdf: {e}",
          status_code=500
      )
    
    try:
      mime_type = 'application/pdf'
      return func.HttpResponse(
          file_stream.read(),
          status_code=200,
          mimetype=mime_type,
          headers={
              'Content-Disposition': f'attachment;filename={"export.pdf"}'
          }
      )
      # return func.HttpResponse(
      #     f"Id is {id}. bearer_token is {bearer_token}. Filepath is {file_path}. This HTTP triggered function executed successfully.",
      #     status_code=200
      # )
    except Exception as e:
      return func.HttpResponse(
          f"Error: {e}",
          status_code=500
      )
        
