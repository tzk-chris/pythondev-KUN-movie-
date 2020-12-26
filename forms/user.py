from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp, ValidationError
from models.userinfo import Userinfo
from werkzeug.security import check_password_hash
from libs.error_code import APIAuthorizedException
from flask import flash, render_template


class RegisterForm(Form):
    """定义用户注册的数据校验"""
    email = StringField(label='邮箱',validators=[DataRequired(message="email是必填的"),
                                    Email(message="邮箱不合法")])
    password = PasswordField(label='密码',validators=[DataRequired(message="password是必填的"),
                                       Regexp(r'^\w{6,18}$', message="密码不符合规范")])
    username = StringField(label='用户名',validators=[DataRequired(message="username是必填的"),
                                                   Regexp(r'^[\w\d_]{3,10}$', message="用户名不符合规范")])

    submit = SubmitField(label='提交')

    def validate_email(self, value):
        # 增加 对email的验证，验证email在数据库中是否存在
        # 如果存在，raise error
        if Userinfo.query.filter_by(email=value.data).first():
            raise ValidationError("邮箱已经被注册")


class LoginForm(Form):
    """定义用户登录的数据校验"""
    email = StringField(label=u'邮箱',validators=[DataRequired(message="email是必填的"),
                                    Email(message="邮箱不合法")])
    password = PasswordField(label=u'密码',validators=[DataRequired(message="password是必填的"),
                                       Regexp(r'^\w{6,18}$', message="密码不符合规范")])

    submit = SubmitField(label=u'提交')

    def validate(self):
        # 增加 对email的验证，验证email在数据库中是否存在
        # 如果存在，raise error
        # 验证邮箱和密码是否对应
        user = Userinfo.query.filter_by(email=self.email.data).first()
        if user and check_password_hash(user.password, self.password.data):
            return user
        else:
            raise APIAuthorizedException



