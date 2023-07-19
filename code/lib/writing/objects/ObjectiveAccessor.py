from parsing import Objective
from writing.objects.BaseAccessor import BaseAccessor
from writing.visitors.BaseAccessorVisitor import BaseAccessorVisitor

class ObjectiveAccessor(BaseAccessor):
    def __init__(self, objective: Objective):
        self.objective = objective
        self.data = {}

        self._init_accessor_data()

    def _init_accessor_data(self) -> None:
        data = {
            # 'id': self.objective.id,
            'objective': self.objective.objective,
            # 'sequence': self.objective.sequence,
        }

        self.data = self._transform_data(data)

    def accept(self, visitor: BaseAccessorVisitor) -> None:
        visitor.visit_objective(self)


    # def get_accessor_data(self) -> dict:
    #     super().get_accessor_data()