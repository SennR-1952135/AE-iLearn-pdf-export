from dataclasses import dataclass

@dataclass
class ScoreRange:
    """Dataclass that represents a score range
    from: the minimum score
    until: the maximum score
    branchNumber: the branch number to go to if the score is in the range
    """
    start: int
    end: int
    branchNumber: int

def scoreRange_from_json(json: dict) -> ScoreRange:
    """ Parse a score range from a json object"""
    return ScoreRange(start=json['from'], end=json['until'], branchNumber=json['branchNumber'])
