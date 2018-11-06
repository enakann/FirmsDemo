import pickle
class Store:
    def __init__(self,fn):
        self.fn=fn
    def read(self):
        fh=open(self.fn,'rb')
        data=pickle.load(fh)
        fh.close()
        return data
    def write(self,msg):
        fw=open(self.fn,'wb')
        pickle.dump(msg,fw)
        fw.close()



s=Store("test")

d=s.read()

d['c']=3

d['hello']="test"
s.write(d)

print(s.read())



