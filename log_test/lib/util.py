import logging
logger=logging.getLogger("kannan")
from . import export

#__all__=['Testa']

@export
class Testa:
    def __init__(self,a,b):
        self.a=a
        self.b=b
    def process(self):
        logger.debug("process is called with {} {}".format(self.a,self.b))
        try:
            return self.a/self.b
        except Exception as e:
            #logger.error(e,exc_info=True)
             logger.exception(e)
