from datetime import datetime
from lib.utils.DBIDTransformer import DBIDTransformer

from lib.parsing.LearningTrack import LearningTrack

from lib.writing.objects.BaseAccessor import BaseAccessor
from lib.writing.objects.ObjectiveAccessor import ObjectiveAccessor
from lib.writing.objects.StepAccessor import StepAccessor
from lib.writing.visitors.BaseAccessorVisitor import BaseAccessorVisitor


class LearningTrackAccessor(BaseAccessor):
    def __init__(self, learning_track: LearningTrack) -> None:
        self.learning_track = learning_track
        self.data = {}
        self.db_key_transformer = DBIDTransformer()
        
        self._init_accessor_data()
        self._transform_ids()
        pass

    def accept(self, visitor: BaseAccessorVisitor) -> None:
        visitor.visit_learning_track(self)

    def _init_accessor_data(self) -> None:
        data = {
              'id': self.learning_track.id,
              'name': self.learning_track.name,
              'createdOn': datetime.strptime(self.learning_track.createdOn, '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%d-%m-%Y'),
              'description': self.learning_track.description,
              # 'enabled': self.learning_track.enabled,
              'startText': self.learning_track.startText,
              'objectives': self._get_objective_accessors(),
              'steps': self._get_step_accessors(),
              'endText': self.learning_track.endText,
          }
        self.data = self._transform_data(data)
       

    # def get_accessor_data(self) -> dict:
    #    super().get_accessor_data()
      
    def _get_objective_accessors(self) -> list[ObjectiveAccessor]:
      objective_accessors = []
      for objective in self.learning_track.objectives:
          objective_accessor = ObjectiveAccessor(objective)
          objective_accessors.append(objective_accessor)

      return objective_accessors
    
    def _get_step_accessors(self) -> list[StepAccessor]:
      step_accessors = []
      for step in self.learning_track.steps:
          step_accessor = StepAccessor(step)
          step_accessors.append(step_accessor)
      
      return step_accessors
    
    def _transform_ids(self) -> None:
      self.db_key_transformer.accessor(self)
      pass
