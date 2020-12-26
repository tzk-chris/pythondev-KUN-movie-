
DEBUG = True
ENV = "development"

# 注意=>Debug这个名字不行
# DEBUG在Flask中有一个默认值为False

# DB配置
import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

HOST = '47.98.33.252'
POST = '3306'
DATABASE = 'web'
USERNAME = 'tzk'
PASSWORD = 'Tzkwan1314='
######
DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(USERNAME,PASSWORD,HOST,POST,DATABASE)
######
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
# SQLALCHEMY_ECHO = True

SECRET_KEY = "this is a secret_key"
EXPIRES_IN = 3600

#### 邮箱配置信息
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = '2069901568@qq.com'
MAIL_PASSWORD = 'xxxxxxxxxx'
