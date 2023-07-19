from parsing import Branch

from writing.objects.BaseAccessor import BaseAccessor
from writing.objects.ScoreRangeAccessor import ScoreRangeAccessor
from writing.visitors.BaseAccessorVisitor import BaseAccessorVisitor

class BranchAccessor(BaseAccessor):
    def __init__(self, branch: Branch) -> None:
        self.branch = branch
        self.data = {}

        self._init_accessor_data()

    def _init_accessor_data(self) -> None:
        data = {
            'branchNumber': self.branch.branchNumber,
            'childStepId': self.branch.childStepId, # f'<a href="#{self.branch.childStepId}">{self.branch.childStepId}</a>',
            'cognition': self.branch.cognition,
            'scoreRange': self._get_score_range_accessors(),
        }

        self.data = self._transform_data(data)

    def accept(self, visitor: BaseAccessorVisitor) -> None:
        visitor.visit_branch(self)

    # def get_accessor_data(self) -> dict:
    #     super().get_accessor_data()

    def _get_score_range_accessors(self) -> list[ScoreRangeAccessor]:
        # There will always be only one score range per branch, but for consistency with other
        # accessors, we return a singleton-list of score range accessors
        score_range_accessor = ScoreRangeAccessor(self.branch.scoreRange)
        return [score_range_accessor] if score_range_accessor.data else []
