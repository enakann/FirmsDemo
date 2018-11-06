import pickle
from pprint import pprint
class Pickling:
    def __init__(self,fn):
        self.fn=fn
        self.fh=open(self.fn,'rb')
        self.fw=open(self.fn,'wb')
    def read(self):
        try:
            data=pickle.load(self.fh)
        except (EOFError,IOError):
            d={'dummy':'data'}
            self.write(d)
            return pickle.load(open(self.fn))
        #self.fh.close()
        if data:
          return data
        #return None
    def write(self,msg):
        if msg:
           pickle.dump(msg,self.fw)
        else:
             d={'dummy':'data'}
             pickle.dump(msg,d)
        #self.fw.close()


if __name__ == '__main__':
    s=Pickling("gen_proxy_db") 

    d=s.read()
    #d={}
    d[23]="headers"
    #d[11111]['payload']="payload"

    d['hello']="test"
    s.write(d)

    pprint(s.read())



