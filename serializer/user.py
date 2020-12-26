from .base import ma
from models.userinfo import Userinfo

class UserSchema(ma.Schema):
    class Meta:
        # 为哪个用户模型创建序列化器
        model = Userinfo
        # 序列化出来的结果有哪些字段
        fields = ('userid', 'username', 'password', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)