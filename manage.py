from operator import imod
from flask_migrate import Migrate, MigrateCommand
from models import Resource
from flask_script import Manager
from server import create_app
from db_session import db
 
app = create_app()      #实例化一个app对象
 
manager = Manager(app)  #实例化一个manager对象
 
Migrate(app, db)    #绑定 数据库与app,建立关系
 
manager.add_command('db', MigrateCommand)    #添加迁移命令集 到脚本命令
 
#如果是以此脚本作为主脚本程序，就执行
if __name__ == '__main__':
    manager.run()