from app import db
from datetime import datetime


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20), unique=True, nullable=False)
    habits = db.relationship('Habit', lazy='dynamic')

    def __init__(self, category):
        self.category = category

    #
    # def __repr__(self):
    #     return self.id, self.category

    def __getitem__(self, index):
        return self.category

    # __getitem__
    # __setitem__
    # __delitem__
    # def __setitem__(self, index, value):
    #     self.bricks.bricksId[index] = value
    @classmethod
    def find_by_category(cls, category):
        return cls.query.filter_by(category=category).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def list_of_ids(cls):
        return cls.id.all()

    @classmethod
    def list_of_ids2(cls, _id):
        return cls.query.filter_by(id=_id)


class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    date_start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_end = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # done = db.Column(db.Boolean, default=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    dates = db.relationship('Date', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.name}', '{self.date_start}')"


class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False, default=datetime.utcnow)
    # db.relationship('Date', lazy='dynamic')

    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id')
                         , nullable=False)

    def __repr__(self):
        return f"Post('{self.date}', '{self.habit_id}')"


class Database:
    @staticmethod
    def list_of_ids(obj):
        list_of_id = []
        for i in db.session.query(obj.id).all():
            list_of_id.append(i[0])
        return list_of_id

    @staticmethod
    def list_of_column(obj, table, _id):
        list_of_col = []
        for i in obj.find_by_id(table, _id):
            list_of_col.append(i)
        return list_of_col

    @staticmethod
    def find_by_id(table, _id):
        return table.query.filter_by(id=_id).first()

    @staticmethod
    def column_with_id(table, column, _id):
        print(table.find_by_id(db.session.query(table._id).all()))
