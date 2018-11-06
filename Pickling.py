import pickle
from pprint import pprint
class Pickling:
    def __init__(self,fn):
        self.fn=fn
    def read(self):
        try:
            fh=open(self.fn,'rb')
            data=pickle.load(fh)
        except (EOFError,IOError):
            raise
    def write(self,msg):
        fw=open(self.fn,'wb')
        pickle.dump(msg,fw)
        fw.close()


if __name__ == '__main__':
    s=Pickling("gen_proxy_db") 

    d=s.read()
    #d={}
    #d[11111]['headers']="headers"
    #d[11111]['payload']="payload"

    #d['hello']="test"
    #s.write(d)

    pprint(s.read())



