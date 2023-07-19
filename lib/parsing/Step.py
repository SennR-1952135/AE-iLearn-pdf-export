from dataclasses import dataclass
from lib.parsing.Question import Question, question_from_json
from lib.parsing.Branch import Branch, branch_from_json

@dataclass
class Step:
    """A step in a learning track
    id: the id of the step
    title: the title of the step
    children: the branches to other steps
    questions: the questions of the step
    type: the type of the step
    instruction(optional): the instruction of the step
    """
    id: str
    title: str
    children: list[Branch]
    questions: list[Question]
    type: str = None # TODO: enum? (what are the possible values?)   
    instruction: str = None
    learningMaterialId: str = None
    learningMaterialIconURL: str = None
    learningMaterialURL: str = None
    learningToolName: str = None
    learningToolId: str = None
    learningMaterialEnabled: bool = None
    learinginActivityTypeId: str = None

def parse_children(json: list) -> list[Branch]:
    """Parse the children of a step"""
    return [branch_from_json(child) for child in json]

def parse_questions(json: list) -> list[Question]:
    """Parse the questions of a step"""
    return [question_from_json(question) for question in json]

def step_from_json(json: dict) -> Step:
    """Parse a step from the json object"""
    children = parse_children(json['children'])
    questions = parse_questions(json['questions'])

    return Step(id=json.get('id', None), title=json.get('title', None), \
                children=children, questions=questions, type=json.get('stepType', None), \
                instruction=json.get('instruction', None), \
                learningMaterialId=json.get('learningMaterial', None), \
                learningMaterialIconURL=json.get('learningMaterialIcon', None), \
                learningMaterialURL=json.get('learningMaterialURL', None), \
                learningToolName=json.get('learningToolName', None), \
                learningToolId=json.get('learningToolId', None), \
                learningMaterialEnabled=json.get('learningMaterialEnabled', None), \
                learinginActivityTypeId=json.get('learinginActivityType', None))