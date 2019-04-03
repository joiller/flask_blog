# 主业务逻辑中的视图和路由的定义
from flask import render_template, request, session, redirect
from . import main  # 导入蓝图程序，用于创建路由
from .. import db  # 导入db 用于操作数据库
from ..models import *  # 导入映射的实体类，用于操作数据库
import time


@main.route('/')
def main_index():
    # user = User.query.filter_by(ID=1).first()
    # topics = Topic.query.filter_by(user=user).all()
    # for topic in topics:
    #     print(topic.title)
    categories = Category.query.all()
    topics = Topic.query.all()
    if 'uid' in session and 'loginname' in session:
        user = User.query.filter_by(ID=session['uid']).first()
    return render_template('index.html', params=locals())


@main.route('/logout')
def logout():
    if 'uid' in session and 'loginname' in session:
        del session['uid']
        del session['loginname']
    return redirect('/login')


@main.route('/login', methods=['GET', 'POST'])
def login_views():
    if request.method=='GET':
        return render_template('login.html')
    else:
        loginname = request.form.get('username')
        upwd = request.form.get('password')
        user = User.query.filter_by(loginname=loginname, upwd=upwd).first()
        if user:
            session['uid'] = user.ID
            session['loginname'] = loginname
            return redirect('/')
        errmsg = '输入错误，请重新输入'
        return render_template('login.html', errmsg=errmsg)


@main.route('/register', methods=['GET', 'POST'])
def register_views():
    if request.method=='GET':
        return render_template('register.html')
    else:
        user = User()
        # print(request.form['loginname'],
        # request.form['email'],
        # request.form['url'],
        # request.form['uname'],
        # request.form['upwd'])
        user.loginname = request.form.get('loginname')
        user.email = request.form.get('email')
        user.url = request.form.get('url')
        user.uname = request.form.get('uname')
        user.upwd = request.form.get('password')
        db.session.add(user)
        # 数据库提交后会自动将提交的数据更新后再复制给user, 但是这里没有提交，在return时才会自动提交
        # 所以这里进行手动提交，以获取user.ID
        db.session.commit()
        print(user.ID)
        session['uid'] = user.ID
        session['loginname'] = user.loginname
        return redirect('/')


@main.route('/release', methods=['GET', 'POST'])
def release_views():
    if request.method == 'GET':
        categories = Category.query.all()
        return render_template('release.html', categories=categories)
    else:
        category_id = request.form.get('category')
        blogtype_id = request.form.get('blogtype')
        content = request.form.get('content')
        title = request.form.get('author')
        picture = request.files['picture']
        pub_date = time.strftime('%Y%m%d%H%M%S')
        topic = Topic()
        if picture:
            file_type = picture.filename.split('.')[-1]
            picture_name = time.strftime('%Y%m%d%H%M%S')
            picture.save('app/static/upload/'+picture_name+'.'+file_type)
            topic.images = 'upload/' + picture_name + '.' + file_type
        topic.pub_date = pub_date
        topic.title = title
        topic.content = content
        topic.blogtype_id = blogtype_id
        topic.category_id = category_id
        db.session.add(topic)
        return redirect('/')


@main.route('/info')
def info():
    tid = request.args.get('topic')
    topic = Topic.query.filter_by(id=tid).first()
    last_topic = Topic.query.filter(Topic.id < tid).order_by('id desc').first()
    next_topic = Topic.query.filter(Topic.id > tid).first()
    topic.read_num += 1
    if 'uid' in session:
        user = User.query.filter_by(ID=session['uid']).first()
    return render_template('info.html', params=locals())
