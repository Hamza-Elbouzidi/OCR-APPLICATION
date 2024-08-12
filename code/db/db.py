from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    json_structure = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    def __repr__(self):
        return f'<Card {self.title}>'
