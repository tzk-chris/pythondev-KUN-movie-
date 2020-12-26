from .base import db


class Movieinfo(db.Model):
    __tablename__ = "movie_info"
    movieid = db.Column("movieid", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.String(32), nullable=False)
    person = db.Column("director_actor", db.String(300), nullable=False)
    info = db.Column("info", db.String(200))
    score = db.Column("score", db.Integer)
    comment = db.Column("comment", db.Integer)
    introduce = db.Column("introduce", db.String(200))
    poster = db.Column("poster", db.String(128))
    like = db.Column("like_num", db.Integer, default=0)

    # 外键关系
    comments = db.relationship('Comments', backref='movie')

