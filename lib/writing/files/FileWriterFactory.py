from lib.writing.files.BaseFileWriter import BaseFileWriter
from lib.writing.files.pdf.PDFWriter import PDFWriter
from lib.writing.files.txt.TXTWriter import TXTWriter

class FileWriterFactory:
    @staticmethod
    def create_writer(file_type:str, filename: str) -> BaseFileWriter:
        if file_type == 'pdf':
            return PDFWriter(filename)
        elif file_type == 'txt':
            return TXTWriter(filename)
        else:
            raise ValueError('Unsupported file type')
