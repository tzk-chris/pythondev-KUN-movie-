

from .view01 import view01_bp
from .movie import movie_bp
# from .v1 import v1_bp

def init_app(app):
    app.register_blueprint(view01_bp)
    app.register_blueprint(movie_bp)
    # app.register_blueprint(v1_bp)
