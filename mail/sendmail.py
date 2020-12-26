# -*- coding: utf-8 -*-
"""
@File  : sendmail.py
@Author: Ekko
@Date  : 2020/8/4 2020/08/04
"""
from flask import current_app
from . import mail
from flask_mail import Message

# 发送邮件函数
def send(receiver:list, subject, body):
    msg = Message(
        subject=subject,
        sender=current_app.config["MAIL_USERNAME"],
        recipients=receiver
    )
    msg.body=body
    mail.send(msg)
    print("end~~")