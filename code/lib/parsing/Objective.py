from dataclasses import dataclass

@dataclass
class Objective:
    """Dataclass that represents an objective
    id: db id of the objective
    objective: description of the objective
    sequence: sequence number of the objective, relevant when multiple objectives are present
    """
    id: str
    objective: str
    sequence: int

def objective_from_json(json: dict) -> Objective:
    """ Parse an objective from a json object
    """
    return Objective(id=json.get('id', None), objective=json.get('objective', None), \
                      sequence=json.get('sequence', None))