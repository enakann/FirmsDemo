class CustomException(BaseException):
    pass

try:
    1/0
except ZeroDivisionError as e:
    raise CustomException(e)


