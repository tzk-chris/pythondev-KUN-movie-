from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g, jsonify
from werkzeug.security import check_password_hash
from models.userinfo import Userinfo
from models.movie_info import Movieinfo
from forms.user import RegisterForm, LoginForm
from forms.comments import PcommentsForm
from os import path
from werkzeug.utils import secure_filename
from config.secure import *
from flask_restful import Resource, Api, reqparse
from libs.handler import  default_error_handler
import jieba


api = Api()
api.handle_error = default_error_handler

view01_bp = Blueprint('view01', __name__)


# from flask import Flask, current_app
# app = current_app()
# 注意：这里用/index/,在浏览器上可以用/index或/index/
# (flask内部做一次重定向) => F12可查看



@view01_bp.route('/')
# @view01_bp.route('/index/')
# @view01_bp.route('/index/index')
def index():
    # 1、从请求头去拿到cookie
    # cookie的获取
    # uid = request.cookies.get('uid', None)
    # 2、session的设置,session底层默认获取传递过来的那个值
    uid = session.get('uid')
    if uid:
        user = Userinfo.query.get(uid)
        return render_template('index.html', user=user, title="首页")
    else:
        return render_template('index.html', title="首页")

# 退出登录
@view01_bp.route('/logout')
def logout():
    response = redirect(url_for('view01.index'))
    # response.delete_cookie('uid')
    del session['uid']
    return response

# 登录
@view01_bp.route('/login', methods=['GET','POST'])
def login():
    data = request.form
    print("login接收的数据： ", data)
    form = LoginForm(data=data)
    if request.method == "POST":
        # it_user = Userinfo.query.filter_by(email=data['email']).first().username
        # session["username"], session["email"] = it_user, data["email"]
        email = data.get('email')
        password = data.get('password')
        users = Userinfo.query.filter(Userinfo.email==email).all()
        for user in users:
            flag = check_password_hash(user.password, password)
            if flag:
                # 1、cookie 的实现机制
                # response = redirect(url_for('view01.index'))
                # #  设置cookie，max_age是登录存在多长时间
                # response.set_cookie('uid', str(user.userid), max_age=1800)
                # return response
                # 2、session的实现机制：session当成字典使用
                session['uid'] = user.userid
                return redirect(url_for('view01.index'))
            else:
                flash("登录失败！邮箱或密码错误")
                return redirect(url_for('view01.login'))
        # if form.validate():
        #     flash("登录成功")
        #     user = Userinfo.query.filter_by(email=data['email']).first().username
        #     session["username"], session["email"] = user, data["email"]
        #     print(session["username"])
        #     return redirect('/?user={}'.format(user))
        # else:
        #     flash("登录失败！")
        #     return  render_template('login.html', msg='邮箱或密码错误')
    return render_template('login.html', title="登录", form=form, user=Userinfo.query.get(session.get('uid')))

# 用户注册
@view01_bp.route('/register', methods=['GET','POST'])
def register():
    data = request.form  # 获取用户传过来的参数（api的参数为json数据）
    form = RegisterForm(data=data)  # 检查参数的合法性（RequestParser/WTForms）
    if form.validate():
        print("验证成功")
        # 创建用户
        user = Userinfo.create_user(email=form.email.data,
                                    username=form.username.data,
                                    password=form.password.data)
        return redirect(url_for('view01.login'))

    return render_template('register.html', title='注册',form=form, user=Userinfo.query.get(session.get('uid')))

# @view01_bp.route('/check_form')
# def check_form():
#     username = request.args.get('itusername')
#     if username:
#         return "可以注册200"
#     else:
#         return "用户名已经被注册"


@view01_bp.route('/center',methods=['GET','POST'])
def center():
    if request.method == 'POST':
        f = request.files['file']
        # basepath = path.abspath(path.dirname(__file__))
        upload_dir = path.join(basedir, 'static')
        f.save(upload_dir, secure_filename(f.filename))
        return redirect(url_for('upload'))
    return render_template('center.html', title="个人中心", user=Userinfo.query.get(session.get('uid')))



# @view01_bp.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         f = request.files['file']
#         # basepath = path.abspath(path.dirname(__file__))
#         upload_dir = path.join(basedir, 'static')
#         f.save(upload_dir, secure_filename(f.filename))
#         return redirect(url_for('upload'))
#     return render_template('upload.html')

# 电影类型
@view01_bp.route('/more')
def more():
    import random
    movies = [Movieinfo.query.get(random.randint(1,251)), Movieinfo.query.get(random.randint(1,251)), Movieinfo.query.get(random.randint(1,251))]
    context = {
        'movies' : movies,
        'user' : Userinfo.query.get(session.get('uid'))
    }
    return render_template('more.html', **context, title="电影类型库")



# 商店：
@view01_bp.route('/shop')
def shop():
    context = {
        "title":"shop"
    }
    return render_template('shop.html', **context)

# 影评：
@view01_bp.route('/single', methods=['GET', 'POST'])
def single():
    myid = request.args.get('id', 1)  #  取出get中的id
    # mymassage = Movieinfo.query.filter_by(movieid=myid).first()   #  通过get请求中的参数找到数据库中对应的数据
    mymassage = Movieinfo.query.get(myid)   #  通过get请求中的参数找到数据库中对应的数据
    form = PcommentsForm()
    context = {
        "form" : form,
        "mymassage" : mymassage,
        "title" : mymassage.name,
        "user" : Userinfo.query.get(session.get('uid')),
    }

    return render_template('single.html', **context)

# 发邮件
from mail.sendmail import send
import random
@view01_bp.route('/sendmail/')
def sendmail():
    uemail = request.args.get('uemail')
    thecode = random.randint(100000,1000000)
    send([uemail], "KUN影网", "验证码{}".format(thecode))
    return "发功成功"







# 接收三种数据：int  float   path路径
# /index/<int:id>
# /index/<myurl>
# /index/<float:num>


# @view01_bp.route('/index/<myurl>')
# def my(myurl):
#     movies = Movieinfo.query.order_by(Movieinfo.movieid).limit(4)
#     # person = Userinfo.query.order_by(Userinfo.name).limit(4)
#     context = {
#         "movies": movies}
#     return render_template('{}.html'.format(myurl), **context)





