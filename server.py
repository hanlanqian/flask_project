from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from sqlalchemy import create_engine
from views import resource, user
from config import Config
from db_session import db




def create_app():
    app = Flask(__name__)
    app.register_blueprint(resource)
    app.register_blueprint(user)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True) ## 跨域问题
    db.init_app(app)                    ## 必须在配置后再创建数据库对象
    return app

app = create_app()


if __name__ == '__main__':
    app.run(port=1234, debug=True)