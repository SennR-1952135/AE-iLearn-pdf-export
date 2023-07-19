from parsing import AnswerOption

from writing.objects.BaseAccessor import BaseAccessor
from writing.visitors.BaseAccessorVisitor import BaseAccessorVisitor
class AnswerOptionAccessor(BaseAccessor):
    def __init__(self, answer_option: AnswerOption) -> None:
        self.answer_option = answer_option
        self.data = {}

        self._init_accessor_data()

    def _init_accessor_data(self) -> None:
        data = {
            # 'id': self.answer_option.id,
            'body': self.answer_option.body,
            'score': self.answer_option.score,
            # 'sequence': self.answer_option.sequence,
        }

        self.data = self._transform_data(data)

    def accept(self, visitor: BaseAccessorVisitor) -> None:
        visitor.visit_answer_option(self)

    # def get_accessor_data(self) -> dict:
    #     super().get_accessor_data()