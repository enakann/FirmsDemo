__all__ =[]


#from . import util
#from . import util2
#from .util import *
#from .util2 import *
#__all__ =[pack1.__all__ + pack2.__all__]
def export(defn):
    
    globals()[defn.__name__]=defn
    __all__.append(defn.__name__)
    return defn


from . import util2
from . import util
