from flask import Flask
import os

def create_app(config=None):
    app = Flask(__name__)

    # 加载配置
    app.config.from_object('config.settings')
    app.config.from_object('config.secure')

    # 加载环境配置
    if 'FLASK_CONF' in os.environ:
        app.config.from_envvar('FLASK_CONF')

    # 加载具体的配置
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)

    # 将序列、数据库、路由挂载到app
    import serializer, models, router, mail
    serializer.init_app(app)
    models.init_app(app)
    router.init_app(app)
    mail.init_app(app)

    return app