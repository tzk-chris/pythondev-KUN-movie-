from .base import ma

def init_app(app):
    ma.init_app(app)

## 注册序列化器到app
