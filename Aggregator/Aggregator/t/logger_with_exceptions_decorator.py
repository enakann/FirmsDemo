
def logger_with_exception_handling(msg,*exp):

    def decorator(f):
        def inner(*args, **kwargs):
                ret=None
                try:
                    logger.info(msg)
                    ret=f(*args, **kwargs)
                except exp as e:
                    print(e)
                    logger.exception(e)
                return ret
        return inner
    return decorator
