from .moda import Testa
from .modb import Testb



def func():
    ls=[]
    p1=Testa(1)
    ret=p1.process()
    ls.append(ret)
    p2=Testb(10)
    ret2=p2.process()
    ls.append(ret2)
    return ls
    

ret=func()
print(ret)
