from app import db


class User(db.Model):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key = True)
  google_id = db.Column(db.String)


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    detail = db.Column(db.String(200))
    deadline = db.Column(db.DateTime)
    individual = db.Column(db.Boolean)
    equality = db.Column(db.Boolean)
    choices = db.relationship('Choice', backref='question', lazy='dynamic')

    def __repr__(self):
        return '<Poll %r>' % (self.title)

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(64))
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))

    votes = db.Column(db.Integer)



    def __repr__(self):
        return '<Choice %r>' % (self.content)

