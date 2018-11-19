import logging
from logwrapper import LogWrapper

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(filename)s(%(lineno)d): "
                    "%(message)s")
logger = logging.getLogger()
lw = LogWrapper(logger)

lw.info('Wrapped well, this is interesting')
