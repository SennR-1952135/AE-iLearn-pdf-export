from parsing import Step
from writing.objects.BaseAccessor import BaseAccessor
from writing.objects.BranchAccessor import BranchAccessor
from writing.objects.QuestionAccessor import QuestionAccessor
from writing.visitors.BaseAccessorVisitor import BaseAccessorVisitor

class StepAccessor(BaseAccessor):
    def __init__(self, step: Step):
        self.step = step
        self.data = {}

        self._init_accessor_data()

    def _init_accessor_data(self) -> None:
        data = {
            'id': self.step.id, #f'<a name="{self.step.id}"/>{self.step.id}',
            'title': self.step.title,
            'type': self.step.type,
            'learningToolName': self.step.learningToolName,
            'learningMaterialURL': self.step.learningMaterialURL, #f'<a href="{self.step.learningMaterialURL}">{self.step.learningMaterialURL.split("?")[0]}</a>' if self.step.learningMaterialURL else None,
            'questions': self._get_question_accessors(),
            'children': self._get_child_accessors(),
        }

        self.data = self._transform_data(data)

    def accept(self, visitor: BaseAccessorVisitor) -> None:
        visitor.visit_step(self)

    def get_accessor_data(self) -> dict:
        data = self.data.copy()
        data['id'] = f'<a name="{data["id"]}"/>{data["id"]}'
        if 'learningMaterialURL' in data:
            data['learningMaterialURL'] = f'<a href="{data["learningMaterialURL"]}">{data["learningMaterialURL"].split("?")[0]}</a>'
        data = self._translate_keys(data)
        return data

    def _get_child_accessors(self) -> list[BranchAccessor]:
        child_accessors = []
        for child in self.step.children:
            child_accessor = BranchAccessor(child)
            child_accessors.append(child_accessor)
        
        return child_accessors
    
    def _get_question_accessors(self) -> list[QuestionAccessor]:
        question_accessors = []
        for question in self.step.questions:
            question_accessor = QuestionAccessor(question)
            question_accessors.append(question_accessor)
        
        return question_accessors