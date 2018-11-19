import logging
import logging.config
from lib import Testa
from lib import Testb
from Logger import Logger
import yaml
from pprint import pprint

#logging.config.fileConfig('configs')
#logger=logging.getLogger('kannan')
#with open ("configsy") as f:
#    config = yaml.safe_load (f)
#logging.config.dictConfig(config)
#logger=logging.getLogger('kannan')
logger_obj=Logger("kannan",r"C:\Users\navkanna\PycharmProjects\aggregator\aggregator\etc\log_config")
logger=logger_obj.get_logger()


def logger_with_exception_handling(*exp):

    def decorator(f):
        def inner(*args, **kwargs):
                ret=None
                try:
                    ret=f(*args, **kwargs)
                except exp as e:
                    print(e)
                    logger.exception(e)
                return ret
        return inner
    return decorator


def func2():
    logger.info("func2 is called")
    ret=1/2
    logger.info(ret)


@logger_with_exception_handling(NameError)
def fun1():
    logger.info("func1 is called")
    func2()
    logger.info("calculating division")
    a/b
    raise ValueError


def main():
    logger.info("program started")
    logger.debug("Testa object is created")
    t=Testa(1,0)
    t.process()
    t2=Testb(0)
    t2.process()
    
    
def func():
    with open("configsy") as f:
        config=yaml.safe_load(f)
    pprint(config)


main()
#func()
#fun1()
#func()
    
