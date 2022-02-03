from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql
import os
pymysql.install_as_MySQLdb()


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', default='wangyuhang123')
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SQLALCHEMY_DATABASE_URI="mysql://root:wyh123456@127.0.0.1/resource?charset=utf8"

files_path = '/home/ubuntu/dev/files'



engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()





    