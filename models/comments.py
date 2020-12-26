from .base import db
from .userinfo import *
from .movie_info import *
from datetime import datetime

class Comments(db.Model):
    __tablename__ = "comments"
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    message = db.Column("message", db.String(400))
    it_time = db.Column("it_time", db.DateTime, default=datetime.now)
    user_id = db.Column("user_id", db.ForeignKey("user_info.userid"), index=True)
    # user_to_id = db.Column("user_to_id", db.ForeignKey("user_info.userid"), index=True)
    movieid = db.Column("movieid", db.ForeignKey("movie_info.movieid"))
    # is_appear = db.Column("is_appear", db.Boolean())   #   是否显示此评论
    # reply_id = db.Column("reply_id", db.Integer, index=True)



