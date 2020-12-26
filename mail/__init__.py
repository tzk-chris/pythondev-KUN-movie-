# -*- coding: utf-8 -*-
"""
@File  : __init__.py.py
@Author: Ekko
@Date  : 2020/8/4 2020/08/04
"""
from flask_mail import Mail

mail = Mail()

def init_app(app):
    mail.init_app(app)