"""定义一个异常捕获器"""

from flask_restful import HTTPException
from libs.error_code import APIException

def default_error_handler(ex):
    # print(ex)
    # 如果返回的异常类，如果是APIException的实例（类/子类）, 返回自己
    if isinstance(ex, APIException):
        return ex
    # 如果返回的是HttpException
    if isinstance(ex, HTTPException):
        code = ex.code
        message = ex.description
        status_code = 10001
        return APIException(code=code, message=message, status_code=status_code)
    return APIException()