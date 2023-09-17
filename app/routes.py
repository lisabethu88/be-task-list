import datetime
from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.helpers import *

# example_bp = Blueprint('example_bp', __name__)

# -------- BOARDS ------
boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

# GET /boards


@boards_bp.route("", methods=["GET"])
def get_all_boards():
    try:
        boards = Board.query.all()
        boards_response = []
        for board in boards:
            boards_response.append(board.to_dict())
    except:
        abort(make_response({"message": "No boards have been created."}, 404))

    return make_response(jsonify(boards_response), 201)


@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    # Validate the board's existence
    board = validate_model(Board, board_id)

    try:
        # Delete the board from the database
        db.session.delete(board)
        db.session.commit()
        return make_response(jsonify({"message": "Board deleted successfully"}), 204)
    except Exception as e:
        # Handle other exceptions
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)

# POST /boards


@boards_bp.route("", methods=["POST"])
def create_a_board():
    board_data = request.get_json()
    try:
        new_board = Board.from_dict(board_data)
        db.session.add(new_board)
        db.session.commit()

    except KeyError as keyerror:
        abort(make_response(
            {"message": f"Request body must include {keyerror.args[0]}."}, 400))

    return make_response(jsonify(new_board.to_dict()), 201)

# GET /boards/<board_id>/cards


@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_all_cards_from_board(board_id):
    board = validate_model(Board, board_id)
    cards = Card.query.filter(Card.board_id == board.id).all()
    cards_response = []
    for card in cards:
        cards_response.append(card.to_dict())

    return make_response(jsonify(cards_response), 200)

# POST /boards/<board_id>/cards


@boards_bp.route("/<board_id>/cards", methods=["POST"])
def add_card_to_board(board_id):
    board = validate_model(Board, board_id)
    card_data = request.get_json()
    print(f"PRINT: {card_data}")
    try:
        new_card = Card.from_dict(card_data, board.id)
        db.session.add(new_card)
        db.session.commit()

    except KeyError as keyerror:
        abort(make_response(
            {"message": f"Request body must include {keyerror.args[0]}."}, 400))

    return make_response(jsonify(new_card.to_dict()), 201)


# ------- CARDS --------
cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

# DELETE /cards/<card_id>


@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card_to_delete = validate_model(Card, card_id)
    db.session.delete(card_to_delete)
    db.session.commit()
    msg = f"Card {card_to_delete.id} successfully deleted"
    return make_response(jsonify({"id": card_to_delete.id, "message": msg}), 200)

# PUT /cards/<card_id>/like


@cards_bp.route("/<card_id>/like", methods=["PUT"])
def update_card_likes(card_id):
    card_to_update = validate_model(Card, card_id)

    card_to_update.likes_count += 1

    try:
        db.session.add(card_to_update)
        db.session.commit()

    except KeyError as keyerror:
        abort(make_response(
            {"message": f"Request body must include {keyerror.args[0]}."}, 400))

    return make_response(jsonify(card_to_update.to_dict()), 200)
