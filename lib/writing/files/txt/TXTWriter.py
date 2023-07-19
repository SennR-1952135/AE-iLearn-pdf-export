from writing.files.BaseFileWriter import BaseFileWriter

class TXTWriter(BaseFileWriter):
    def __init__(self, filename):
        self.filename = filename
        self.file_type = 'txt'
        self.file = open(self.filename, 'w')

    def __del__(self):
        self.file.close()

    def write(self, str) -> None:
        self.file.write(str)
    
    def write_pair(self, key, value) -> None:
        self._add_content(key, value)
            
    def _add_content(self, key, value) -> None:
        # # If the value is a list of BaseWriter instances, call write() on each
        # # First check needed to avoid looping over strings
        # if isinstance(value, list) and all(isinstance(instance, BaseWriter) for instance in value):
        #     self.file.write(f'{key}:\n')
        #     for writer in value:
        #         # indent the content
        #         writer.write(self.file_type, self.file)               
        # # otherwise, just write the key and value
        # else:
        #     self.file.write(f'{key}: {value}\n')
        self.file.write(f'{key}: {value}\n')