from libs.error_code import Success

def generate_response(data, message=Success.message, status_code=Success.status_code):
    return {
        "message": message,
        "status_code": status_code,
        "data": data
    }
