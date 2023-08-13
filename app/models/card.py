from app import db

class Card(db.Model):
    __tablename__ = "card"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "likes_count": self.likes_count,
            "board_id": self.board_id
        }

    @classmethod
    def from_dict(cls, card_data, board_id):
        new_card = Card(
            message = card_data["message"],
            likes_count = card_data["likes_count"],
            board_id = board_id
        )
        return new_card
