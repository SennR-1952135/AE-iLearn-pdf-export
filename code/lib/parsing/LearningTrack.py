from dataclasses import dataclass
from parsing.Step import Step, step_from_json
from parsing.Objective import Objective, objective_from_json

@dataclass
class LearningTrack:
    """Dataclass that represents a learning track
    id: db id of the learning track
    name: name of the learning track
    description: description of the learning track
    enabled: is this learning track currently enabled
    startText: introduction text of the learning track
    endText: conclusion text of the learning track
    steps: list of steps of the learning track (see Step.py)
    createdOn: date the learning track was created, format: yyyy-MM-dd'T'HH:mm:ss.SSSZ
    objectives: list of objectives of the learning track (see Objective.py)
    """
    id: str
    name: str
    description: str
    enabled: bool
    startText: str
    endText: str
    steps: list[Step]
    createdOn: str
    objectives: list[Objective]

def learningtrack_from_json(json: dict) -> LearningTrack:
    """ Parse a learning track from a json object
    """
    steps = [step_from_json(step) for step in json['steps']]
    objectives = [objective_from_json(objective) for objective in json['learningTrackObjectives']]

    return LearningTrack(id=json.get('id', None), name=json.get('name', None), \
                          description=json.get('description', None), enabled=json.get('enabled', None), \
                          startText=json.get('startText', None), endText=json.get('endText', None), \
                          steps=steps, createdOn=json.get('createdOn', None), objectives=objectives)