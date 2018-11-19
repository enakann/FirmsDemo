import logging
import traceback
logger=logging.getLogger("kannan")
import sys
from . import export

@export
class Testb:
    def __init__(self,a):
        self.a=a
    def process(self):
        try:
           return self.a*self.b
        except Exception as e:
            tb=traceback.extract_stack()
            logger.error(tb)
            print(tb)
            
