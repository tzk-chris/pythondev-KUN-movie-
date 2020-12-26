
from app import create_app

app = create_app()

if __name__ == '__main__':
    # from werkzeug.contrib.fixers import ProxyFix
    # app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(host='0.0.0.0', port=5000, debug=app.config["DEBUG"])
