from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g, jsonify
from sqlalchemy import or_, and_
from models.userinfo import Userinfo
from models.movie_info import Movieinfo
from models.comments import Comments
from models.base import db
from flask_restful import Resource, Api, reqparse
from libs.handler import  default_error_handler


api = Api()
api.handle_error = default_error_handler

movie_bp = Blueprint('movie', __name__)

# 电影列表
@movie_bp.route('/movie')
def movie():
    # page
    # 当前页数
    # per_page
    # 每页显示的条�?
    # error_out
    # 是否打印错误信息
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))  # 这里�?0 决定每页显示的数目，可自行调�?
    paginate = Movieinfo.query.order_by(Movieinfo.movieid).paginate(page, per_page, error_out=False)
    movies = paginate.items   #  拿到分页后的数据

    context = {
        "movies" : movies,
        "paginate" : paginate,
        "user" : Userinfo.query.get(session.get('uid'))
    }
    return render_template('movie.html', **context, title="movie")

# 发表影评�?
@movie_bp.route('/add_comment', methods=['POST', 'GET'])
def add_comment():
    if request.method == 'POST':
        comment_content = request.form.get('comment')
        user_id = Userinfo.query.filter_by(userid=session.get('uid', None)).first().userid
        print(user_id)
        movie_id = request.form.get('id')

        # 评论模型
        comment = Comments()
        comment.message = comment_content
        comment.user_id = user_id
        comment.movieid = movie_id
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('view01.single')+"?id="+movie_id)
    return render_template(url_for('movie.movie'))

# 点赞
@movie_bp.route('/like')
def like():
    tag = request.args.get('tag', None)
    movie_id = request.args.get('aid', None)
    movie1 = Movieinfo.query.get(movie_id)
    # 设置一个用户对同一部电影只能点赞一�?
    if tag == '1':
        movie1.like -= 1
    else:
        movie1.like += 1
    db.session.commit()
    return jsonify(num=movie1.like)

# 搜索
@movie_bp.route('/search')
def search():
    keyword = request.args.get('search', None)
    if keyword == '':
        return redirect(url_for('movie.movie'))

    # 查询
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))# 这里�?0 决定每页显示的数目，可自行调�?
    paginate = Movieinfo.query.filter(or_(Movieinfo.name.contains(keyword), Movieinfo.info.contains(keyword), Movieinfo.person.contains(keyword))).paginate(page, per_page, error_out=False)
    movies = paginate.items
    context = {
        "movies": movies,
        "paginate": paginate,
        "user": Userinfo.query.get(session.get('uid'))
    }
    return render_template('movie.html', **context, title="查询"+keyword+"结果")

# 类型查询
@movie_bp.route('/type')
def movie_type():

    my_type = request.args.get('word', '')  #  获得url中的电影类型的参数�?
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 250))  # 这里�?0 决定每页显示的数目，可自行调�?
    paginate = Movieinfo.query.filter(Movieinfo.info.contains(my_type)).paginate(page, per_page, error_out=False)
    movies = paginate.items
    context = {
        'movies' : movies,
        "paginate": paginate,
        "user": Userinfo.query.get(session.get('uid'))
    }
    return render_template('movie.html', **context, title=my_type)
    

@movie_bp.route('/scan')
def scan():
    scan_id = request.args.get('scan')
    return render_template('scan.html', scan_movie=scan_id)

@movie_bp.route('/video')
def video():
    return render_template('video.html', title="视频")
