# 与当前项目相关的模型文件，即所有的实体类
from . import db


class BlogType(db.Model):
    __tablename__ = 'blogtype'
    id = db.Column(db.INTEGER, primary_key=True)
    type_name = db.Column(db.String(20))
    topic = db.relationship('Topic', backref='blogtype', lazy='dynamic')

    def __init__(self, n):
        self.type_name = n

    def __repr__(self):
        return 'BlogType : %r' % self.type_name


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.INTEGER, primary_key=True)
    cate_name = db.Column(db.String(50))
    topic = db.relationship('Topic', backref='category', lazy='dynamic')

    def __init__(self, n):
        self.cate_name = n

    def __repr__(self):
        return 'Category : %r' % self.cate_name


class User(db.Model):
    __tablename__ = 'user'
    ID = db.Column(db.INTEGER, primary_key=True)
    loginname = db.Column(db.String(50), nullable=False)
    uname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200))
    upwd = db.Column(db.String(30), nullable=False)
    is_author = db.Column(db.SmallInteger, default=0)
    topic = db.relationship('Topic', backref='user', lazy='dynamic')
    reply = db.relationship('Reply', backref='user', lazy='dynamic')
    voke_topic = db.relationship(
        'Topic',
        secondary='voke',
        backref=db.backref('voke_user', lazy='dynamic'),
        lazy='dynamic'
    )

    # def __init__(self, n):
    #     self.uname = n
    #
    def __repr__(self):
        return 'User : %r' % self.uname


class Topic(db.Model):
    __tablename__ = 'topic'
    id = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False)
    read_num = db.Column(db.INTEGER, default=0)
    content = db.Column(db.Text, nullable=False)
    images = db.Column(db.Text)
    blogtype_id = db.Column(db.INTEGER, db.ForeignKey('blogtype.id'))
    category_id = db.Column(db.INTEGER, db.ForeignKey('category.id'))
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.ID'))
    reply = db.relationship('Reply', backref='topic', lazy='dynamic')

    # def __init__(self, n):
    #     self.cate_name = n
    #
    # def __repr__(self):
    #     return 'Category : %r' % self.cate_name


class Reply(db.Model):
    __tablename__ = 'reply'
    id = db.Column(db.INTEGER, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    reply_time = db.Column(db.DateTime)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.ID'))
    topic_id = db.Column(db.INTEGER, db.ForeignKey('topic.id'))

    # def __init__(self, n):
    #
    # def __repr__(self):
    #     return 'Category : %r' % self.cate_name

Voke = db.Table(
    'voke',
    db.Column('id', db.INTEGER, primary_key=True),
    db.Column('user_id', db.INTEGER, db.ForeignKey('user.ID')),
    db.Column('topic_id', db.INTEGER, db.ForeignKey('topic.id'))
)