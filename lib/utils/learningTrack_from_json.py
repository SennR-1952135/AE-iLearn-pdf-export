from lib.utils.augment_learningTrack_json import augment_learningTrack_json
from lib.utils.DBIDTransformer import DBIDTransformer
from lib.parsing.LearningTrack import learningtrack_from_json

def learningTrack_from_json(lt_json: dict):
    augment_learningTrack_json(lt_json)
    transformer = DBIDTransformer() # TODO is this necessary?
    transformer.json(lt_json)
    # parse learning track to object LearningTrack object
    lt = learningtrack_from_json(lt_json)
    return lt