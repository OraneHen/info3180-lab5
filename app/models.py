from . import db

class Movies(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.Text)
    poster = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, title, description, poster):
        self.title = title
        self.description = description
        self.poster = poster

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support