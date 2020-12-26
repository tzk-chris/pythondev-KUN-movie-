from .base import db
from werkzeug.security import generate_password_hash
import random
import string
from .comments import *


class Userinfo(db.Model):
    __tablename__ = "user_info"
    userid = db.Column("userid", db.Integer, primary_key=True, autoincrement=True)
    username = db.Column("username", db.String(32))
    _password = db.Column("password", db.String(128))
    email = db.Column("email", db.String(64), unique=True)
    icon = db.Column("icon", db.String(100))   #  头像

    # user_to_id = db.relationship('Comments', foreign_keys=[Comments.user_to_id],
    #                              backref=db.backref('user_to', lazy='joined'), lazy='dynamic')
    posts = db.relationship('Comments', foreign_keys=[Comments.user_id],
                                 backref=db.backref('userid', lazy='joined'),lazy='dynamic')

    # 属性包装
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        # value => 传过来的明文密码
        self._password = generate_password_hash(value)

    @classmethod
    def create_user(cls, email, username, password):

            user = cls()
            user.email = email
            user.username = username if username else "".join(random.choices(string.ascii_letters,k=8))
            user.password = password
            db.session.add(user)
            db.session.commit()
            return user


