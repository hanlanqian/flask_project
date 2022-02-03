from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from sqlalchemy import create_engine
from views import resource
from config import Config
from db_session import db


def create_app():
    app = Flask(__name__)
    app.register_blueprint(resource)
    app.config.from_object(Config)
    db.init_app(app)                    ## 必须在配置后再创建数据库对象
    return app

app = create_app()


if __name__ == '__main__':
    app.run(port=1234, debug=True)