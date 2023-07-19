from dataclasses import dataclass
from parsing.Question import Question, question_from_json
from parsing.ScoreRange import ScoreRange, scoreRange_from_json

@dataclass
class Branch:
    """A branch from a step to another step
    branchNumber: the branch number
    childStepId: the id of the step to go to
    cognition: the cognition level of the branch
    scoreRange: the score range to check
    """
    branchNumber: int
    childStepId: str
    cognition: str = None #TODO: enum
    scoreRange: scoreRange = None
        
def branch_from_json(json: dict) -> Branch:
    scoreRange = scoreRange_from_json(json['scoreRange']) if 'scoreRange' in json else None
    return Branch(branchNumber=json.get('branchNumber', None), \
                  childStepId=json.get('childStepId', None), \
                  cognition=json.get('cognition', None), scoreRange=scoreRange)

