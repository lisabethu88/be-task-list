from flask import abort, make_response, request
from app.models.board import Board
from app.models.card import Card


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))
    model = cls.query.get(model_id)
    if model:
        return model 
    abort(make_response({"message": f"{cls.__name__} {model_id} was not found"}, 404))