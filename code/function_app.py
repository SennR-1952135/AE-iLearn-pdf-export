import azure.functions as func
from _azure.export_pdf.main import export_pdf_bp

app = func.FunctionApp()
app.register_functions(export_pdf_bp)


@app.function_name('hello')
def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        "Hello, World! This HTTP triggered function executed successfully.",
        status_code=200
    )


# create new test function
app.register_functions(func.HttpResponse("Hello, World! This HTTP triggered function executed successfully."))