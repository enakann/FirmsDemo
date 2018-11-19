import logging
import random
import os
class myFileHandler(logging.FileHandler):
    def __init__(self,path,fileName,mode):
        r = random.randint(1,100000)
        path = path+"/log_"+str(r)
        os.mkdir(path)
        super(myFileHandler,self).__init__(path+"/"+fileName,mode)
