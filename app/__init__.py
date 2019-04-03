# 对整个应用做初始化
# 主要工作：
# 1、构建flask应用以及各种配置
# 2、构建SQLAlchemy的应用

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['DEBUG']=True  # 调试模式
    app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:jhl233666@localhost:3306/dblog'  # 连接数据库
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True  # 设置数据库在内容更新时自动提交
    app.config['SECRET_KEY']='NINCAICAIKANYA'  # 设置session秘钥
    db.init_app(app)  # 数据库的初始化
    from .main import main as main_blueprint  # 将app与main关联到一起
    app.register_blueprint(main_blueprint)
    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)
    return app
