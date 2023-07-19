from lib.writing.visitors.BaseAccessorVisitor import BaseAccessorVisitor
from lib.writing.objects.LearningTrackAccessor import LearningTrackAccessor
from lib.writing.objects.BaseAccessor import BaseAccessor
from lib.utils.graph import LearningTrackGraph

class PDFAccessorVisitor(BaseAccessorVisitor):
    
    def __init__(self, filename: str) -> None:
        super().__init__("pdf", filename)

        # additonal attributes
        self.indent = 0

    def _process_data(self, data: dict) -> None:
        for k, v in data.items():
            if isinstance(v, list) and all(isinstance(instance, BaseAccessor) for instance in v):
                self.file_writer.write(f'{k}:', self.indent)
                self.indent += 1
                # self.file_writer.write('-----', self.indent)
                for writerObj in v:
                    # self.file_writer.write('-   ', self.indent, no_trailing_newline=True)
                    # self.file_writer.write('\n', self.indent)
                    # self.indent += 1
                    writerObj.accept(self)
                    # self.file_writer.write('-----', self.indent)
                    # self.file_writer.write('\n', self.indent)
                self.indent -= 1
            else:
                self.file_writer.write_pair(k, v, self.indent)

    def visit_learning_track(self, learning_track_accessor: LearningTrackAccessor) -> None:
        ltg = LearningTrackGraph(learning_track_accessor.learning_track)
        key_mapping = learning_track_accessor.db_key_transformer.get_key_mapping()
        self.file_writer.add_LearningTrack_graph(ltg, key_mapping)
        data = learning_track_accessor.get_accessor_data()
        self._process_data(data)



