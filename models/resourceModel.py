from config import Base
from sqlalchemy import Column, Integer, String, Float, Date
from db_session import db
from flask import Response, abort
from utils import UnitBase

class Resource(UnitBase):
    __tablename__ = 'Resource'
    id = db.Column(Integer, primary_key=True)
    file_name = db.Column(String(64), nullable=False, unique=True)
    file_size = db.Column(Float, nullable=False)


    @classmethod
    def get_or_404(cls, file_name):
        m = cls.query.filter_by(file_name=file_name).all()
        if not m:
            abort(Response("404ERROR! 没有找到对应id的资源"))
        else:
            return m

    @classmethod
    def get_or_none(cls, file_name):
        m = cls.query.filter_by(file_name=file_name).all()
        if not m:
            return None
        else:
            return m

    @classmethod
    def upsert(cls, data: dict):
        file_name = data.get('file_name', None)
        file = cls.get_or_none(file_name)
        if not file:
            file = cls(file_name=file_name, file_size=data.get('file_size', 0))
            db.session.add(file)
            db.session.commit()
        else:
            file = cls.query.filter_by(file_name=file_name)
            file.update({'file_size': data.get('file_size', 0)})
            file = file.all()
        return file
            