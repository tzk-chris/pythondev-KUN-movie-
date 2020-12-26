"""定义异常信息，有便于我们对于异常信息的收集"""

import json
from werkzeug.exceptions import HTTPException

class APIException(HTTPException):
    """通用的异常信息类"""
    # code => http状态码， status_code => 业务状态码
    code = 500
    message = "oops!"
    status_code = 99999

    def __init__(self, message=None, code=None, status_code=None):
        if message:
            self.message = message
        if code:
            self.code = code
        if status_code:
            self.status_code = status_code
        super().__init__(description=message)


    def get_body(self, environ=None):
        """标准化的异常数据格式"""
        body = {
            "message": self.message,
            "status_code": self.status_code
        }
        content = json.dumps(body)
        return content

    def get_headers(self, environ=None):
        """告诉浏览器，返回json格式数据"""
        return [("Content-Type", "application/json")]


class Success(APIException):
    """自定义异常类测试"""
    message = "OK!"
    status_code = 10000


class FormValidateException(APIException):
    """自定义异常类测试"""
    message = "表单验证失败"
    status_code = 10002


class ArgsTypeException(APIException):
    """自定义异常类测试"""
    message = "表单提交数据格式不正确"
    status_code = 10003


class APIAuthorizedException(APIException):
    code = 401
    message = "用户认证失败"
    status_code = 10004