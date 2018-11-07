def retry(retries=3):
    left = {'retries': retries}

    def decorator(f):
        def inner(*args, **kwargs):
            while left['retries']:
                try:
                    return f(*args, **kwargs)
                except NameError as e:
                    print e
                    left['retries'] -= 1
                    print "Retries Left", left['retries']
            raise Exception("Retried {} times".format(retries))
        return inner
    return decorator


