from app import db
from datetime import datetime
import re


def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)


class Citizen(db.Model):
    citizen_id = db.Column(db.Integer)
    town = db.Column(db.String(257))
    street = db.Column(db.String(257))
    building = db.Column(db.String(257))
    apartment = db.Column(db.Integer)
    name = db.Column(db.String(257))
    birth_date = db.Column(db.DateTime)
    gender = db.Column(db.String(7))
    relatives = db.Column(db.PickleType())
    import_id = db.Column(db.Integer)
    intern_id = db.Column(db.Integer, unique=True, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, *args, **kwards):
        super(Citizen, self).__init__(*args, **kwards)

    def __repr__(self):
        return '<Post id: {}, name: {}>'.format(self.citizen_id, self.name)

