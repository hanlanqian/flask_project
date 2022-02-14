from turtle import clear
from sqlalchemy import Integer, String, Float, true
from db_session import db
from flask import Response, abort
from utils import UnitBase
from config import files_path
import os

class Resource(UnitBase):
    __tablename__ = 'Resource'
    id = db.Column(Integer, primary_key=True)
    file_name = db.Column(String(64), nullable=False, unique=True)
    file_size = db.Column(Float, nullable=False)
    file_type = db.Column(String(32), default='unknown')

    @classmethod
    def get_all(cls):
        _ms = cls.query.all()
        ms = []
        for m in _ms:
            ms.append(m.to_dict())
        return ms

    @classmethod
    def get_or_404(cls, key):
        # 通过id或者file_name获取示例数据
        m = cls.query.filter_by(file_name=key).all()
        if not m:
            m = cls.query.filter_by(id=key).all()
            if not m:
                abort(Response("404ERROR! 没有找到对应id的资源"))
            else:
                return m
        else:
            return m

    @classmethod
    def get_or_none(cls, key):
        # 通过id或者file_name获取示例数据
        m = cls.query.filter_by(file_name=key).all()
        if not m:
            m = cls.query.filter_by(id=key).all()
            if not m:
                return None
            else:
                return m
        else:
            return m

    @classmethod
    def upsert(cls, data: dict):
        file_name = data.get('file_name', None)
        file = cls.get_or_none(file_name)
        if not file:
            cls.insert(data)
        else:
            file[0].update(data)
        return file
    
    @classmethod
    def delete(cls, key):
        if isinstance(key, int):
            cls.query.filter(Resource.id==key).delete()
            db.session.commit()
        elif isinstance(key, str):
            cls.query.filter(Resource.file_name==key).delete()
            db.session.commit()
        else:
            return abort(Response("wrong type for delete key"))
        os.remove(f"{files_path}/{key}")
        return 'successfully delete'


