from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Dictionary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(100), nullable=False)
    chinese = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Dictionary {self.english}>'