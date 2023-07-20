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