from parsing import Question
from writing.objects.BaseAccessor import BaseAccessor
from writing.objects.AnswerOptionAccessor import AnswerOptionAccessor
from writing.visitors.BaseAccessorVisitor import BaseAccessorVisitor

class QuestionAccessor(BaseAccessor):
    def __init__(self, question: Question):
        self.question = question
        self.data = {}

        self._init_accessor_data()

    def _init_accessor_data(self) -> None:
        data = {
            # 'id': self.question.id,
            'body': self.question.body,
            'answerOptions': self._get_answer_option_accessors(),
            # 'sequence': self.question.sequence,
        }

        self.data = self._transform_data(data)
    
    def accept(self, visitor: BaseAccessorVisitor) -> None:
        visitor.visit_question(self)

    # def get_accessor_data(self) -> dict:
    #     super().get_accessor_data()
    
    def _get_answer_option_accessors(self) -> list[AnswerOptionAccessor]:
        answer_option_accessors = []
        for answer_option in self.question.answerOptions:
            answer_option_accessor = AnswerOptionAccessor(answer_option)
            answer_option_accessors.append(answer_option_accessor)
        
        return answer_option_accessors