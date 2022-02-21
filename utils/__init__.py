from time import sleep
from db_session import db
from sqlalchemy import text, TIMESTAMP
import datetime
from flask import Response, abort


class UnitBase(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, nullable=False)

    @classmethod
    def insert(cls, data:dict):
        pop_key = []
        for key, value in data.items():
            if not hasattr(cls, key):
                pop_key.append(key)
        [data.pop(i) for i in pop_key]
        m = cls(**data)
        db.session.add(m)
        db.session.commit()
        return m


    def update(self, data:dict):
        pop_key = []
        for key, value in data.items():
            if not hasattr(self, key):
                pop_key.append(key)
        [data.pop(i) for i in pop_key]
        data.update({'update_time': datetime.datetime.now()})
        self.query.filter(getattr(self.__class__, 'id')==getattr(self, 'id')).update(data)
        db.session.commit()
        return self

    def to_dict(self):
        data = self.__dict__
        data.pop('_sa_instance_state')
        return data
