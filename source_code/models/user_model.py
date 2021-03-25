from source_code.db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Application programming interface
    @classmethod
    def find_by_user_name(cls, user_name):
        return cls.query.filter_by(user_name=user_name).first()

    # Application programming interface
    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(id=_id).first()