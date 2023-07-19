from lib.writing.visitors.BaseAccessorVisitor import BaseAccessorVisitor
from lib.writing.objects.BaseAccessor import BaseAccessor

class TXTAccessorVisitor(BaseAccessorVisitor):
    
    def __init__(self, filename: str) -> None:
        super().__init__("txt", filename)

        # additonal attributes
        self.indent = 0

    def _process_data(self, data: dict) -> None:
        for k, v in data.items():
            if isinstance(v, list) and all(isinstance(instance, BaseAccessor) for instance in v):
                self.file_writer.write(f'{self.indent * 4 * " "}')
                self.file_writer.write(f'{k}: {{\n')
                self.indent += 1
                for writerObj in v:
                    self.file_writer.write(f'{self.indent * 4 * " "}')
                    self.file_writer.write('{\n')
                    self.indent += 1
                    writerObj.accept(self)
                    self.indent -= 1
                    self.file_writer.write(f'{self.indent * 4 * " "}')
                    self.file_writer.write('},\n')
                self.indent -= 1
                self.file_writer.write(f'{self.indent * 4 * " "}')
                self.file_writer.write('}\n')
            else:
                self.file_writer.write(f'{self.indent * 4 * " "}')
                self.file_writer.write_pair(k, v)