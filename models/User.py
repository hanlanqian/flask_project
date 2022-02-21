from logging.handlers import DatagramHandler
from sqlalchemy import Integer, String, Float
from db_session import db
from flask import Response, abort, g
from utils import UnitBase
from config import files_path, Config

from passlib.hash import pbkdf2_sha256
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature
import uuid

class User(UnitBase):
    __tablename__ = 'User'
    id = db.Column(Integer, primary_key=True)
    uid = db.Column(String(64), nullable=False, unique=True)
    age = db.Column(Integer, nullable=True)
    username = db.Column(String(64), nullable=False, unique=True)
    password = db.Column(String(256), nullable=False)
    email = db.Column(String(64))
    phoneNumber = db.Column(String(64))



    @classmethod
    def authLogin(cls, data: dict):
        username = data.get("username", "")
        ms = cls.query.filter_by(username=username).all()
        if not ms:
            return abort(Response("不存在该用户名"))
        elif not pbkdf2_sha256.verify(data.get("password"), ms[0].password):
            return abort(Response("密码错误"))
        else:
            token = cls.generate_token()
            return dict(token=token, uid=ms[0].uid)

    @classmethod
    def register(cls, data: dict):
        username = data.get("username", "")
        ms = cls.query.filter_by(username=username).all()
        if ms:
            return abort(Response("用户名已存在"))
        else:
            password = data.pop("password")
            password = pbkdf2_sha256.hash(password)
            data['password'] = password
            data['uid'] = uuid.uuid4()
            m = cls.insert(data)
            return m
    
    def generate_token():
        TimedJSONWebSignatureSerializer(Config.SECRET_KEY, expires_in=600)
        
        return 