import azure.functions as func
from _azure.export_pdf.main import export_pdf_bp

app = func.FunctionApp()
app.register_functions(export_pdf_bp)