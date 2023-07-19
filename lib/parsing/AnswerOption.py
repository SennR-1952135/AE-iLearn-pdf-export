from dataclasses import dataclass

@dataclass
class AnswerOption:
    """Dataclass that represents an answer option
    id: db id of the answer option
    body: the body of the answer option (the text)
    score: the score of the answer option
    sequence: the sequence number of the answer option (relevant when multiple answer options are present)"""
    id: str
    body: str
    score: int
    sequence: int

def answeroption_from_json(json: dict) -> AnswerOption:
    """ Parse an answer option from a json object"""
    return AnswerOption(id=json.get('id', None), body=json.get('body', None), \
                        score=json.get('score', None), sequence=json.get('sequence', None))
