# user 目录：针对用户业务逻辑处理的目录
# 针对用户业务逻辑处理的初始化操作
from flask import Blueprint

user = Blueprint('user', __name__)
from . import views