from dataclasses import dataclass
from lib.parsing.AnswerOption import AnswerOption, answeroption_from_json

@dataclass
class Question:
    """Dataclass that represents a question
    id: the id of the question
    body: the body of the question (the text)
    answerOptions: the answer options of the question
    sequence: the sequence number of the question (relevant when multiple questions are present)"""
    id: str
    body: str
    answerOptions: list[AnswerOption]  
    sequence: int  

def question_from_json(json: dict) -> Question:
    """ Parse a question from a json object"""
    answerOptions = [answeroption_from_json(answerOption) \
                     for answerOption in json['answerOptions']]
    
    return Question(id=json.get('id', None), body=json.get('body', None), \
                    answerOptions=answerOptions, sequence=json.get('sequence', None))