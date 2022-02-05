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


    def update(self, data:dict):
        for key, value in data.items():
            if not hasattr(self, key):
                abort(Response(f"表格{self.__tablename__}没有{key}属性"))
        data.update({'update_time': datetime.datetime.now()})
        self.query.filter(getattr(self.__class__, 'id')==getattr(self, 'id')).update(data)
        db.session.commit()
        return self

    def to_dict(self):
        data = self.__dict__
        data.pop('_sa_instance_state')
        print(data)
        return 0
