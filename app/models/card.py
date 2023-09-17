from app import db


class Card(db.Model):
    __tablename__ = "card"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"))
    board = db.relationship("Board", back_populates="cards")
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    image = db.Column(db.String, nullable=True,
                      default="")  # Optional image column

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "likes_count": self.likes_count,
            "board_id": self.board_id,
            "date": self.date,
            "image": self.image
        }

    @classmethod
    def from_dict(cls, card_data, board_id):
        new_card = Card(
            message=card_data["message"],
            likes_count=card_data["likes_count"],
            board_id=board_id,
            date=card_data["date"],
            image=card_data["image"]
        )
        return new_card
