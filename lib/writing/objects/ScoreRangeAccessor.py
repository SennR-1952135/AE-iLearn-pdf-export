from parsing import ScoreRange
from writing.objects.BaseAccessor import BaseAccessor
from writing.visitors.BaseAccessorVisitor import BaseAccessorVisitor

class ScoreRangeAccessor(BaseAccessor):
    def __init__(self, score_range: ScoreRange):
        self.score_range = score_range
        self.data = {}

        self._init_accessor_data()

    def _init_accessor_data(self) -> None:
        if self.score_range is None:
            self.data = {}
            return

        data = {
            'start': self.score_range.start,
            'end': self.score_range.end,
            'branchNumber': self.score_range.branchNumber,
        }

        self.data = self._transform_data(data)

    def accept(self, visitor: BaseAccessorVisitor) -> None:
        visitor.visit_score_range(self)

    # def get_accessor_data(self) -> dict:
    #     super().get_accessor_data()