import os
import yaml
import logging
import logging.config

LOG_ROOT=r"C:\Users\navkanna\PycharmProjects\FirmsDemo\Aggregator\Aggregator\logs"

def logmaker_error():
    path=LOG_ROOT
    path = os.path.join(path, 'error.log')
    #return logging.FileHandler(path)
    return logging.handlers.RotatingFileHandler(path)

def logmaker_info():
    path=LOG_ROOT
    path = os.path.join(path, 'error.log')
    return logging.FileHandler(path)





