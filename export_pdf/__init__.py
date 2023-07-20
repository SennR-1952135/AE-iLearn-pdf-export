import logging
import azure.functions as func
from .utils import get_param, export_pdf


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
      file_path = export_pdf(id, bearer_token)
      file_path = file_path.replace('/home/site/wwwroot/', '')
    except Exception as e:
      return func.HttpResponse(
          f"Error exporting pdf: {e}",
          status_code=500
      )
    
    try:
      with open(file_path, 'rb') as f:
        mime_type = 'application/pdf'
        return func.HttpResponse(
            f.read(),
            status_code=200,
            mimetype=mime_type,
            headers={
                'Content-Disposition': f'attachment;filename={file_path}'
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
        
