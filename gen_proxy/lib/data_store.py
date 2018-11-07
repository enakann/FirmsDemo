from Pickling import Pickling

class DataStore:
    def __init__(self,prop,msg):
        self.prop=prop.headers
        self.msg=msg
        self.pickle=Pickling(r"/home/navi/Dev_backup/Dev/gen_proxy/lib/gen_proxy_db")
        self.correlation_id=None

    def process(self):
        print("In process")
        self.correlation_id=self.get_corrid()
        try:
           print("1 receiced data from picking")
           data=self.pickle.read()
           #pprint("2 recevied data is {}".format(data))
           #data={}
        except Exception as e:
            print("Receieved Exception:{ } from Pickling".format(e))
            raise e
        if data:
            print("in if data block")
            print(data)
            if self.correlation_id in data.keys():
                    #msgAndHeader=data.get(self.correlation_id,None)
                    msgAndHeader=data.pop(self.correlation_id)
                    if data:
                       self.pickle.write(data)
                       print(data)
                    else:
                        data={'dummy':'d'}
                        self.pickle.write(data)
                    return msgAndHeader
            else:
                print("in else of the if data part")
                data[self.correlation_id]={}
                data[self.correlation_id]['headers']=self.prop
                data[self.correlation_id]['payload']=self.msg
                try:
                    self.pickle.write(data)
                    print(data)
                except Exception as e:
                   raise e
                return True
        else:
            print("in else part Datastore")
            data={}
            data[self.correlation_id]={}
            data[self.correlation_id]['headers']=self.prop
            data[self.correlation_id]['payload']=self.msg
            self.pickle.write(data)
            print("else part picking done")
            return True
        #return False


    def get_corrid(self):
        print("in get_corrid block")
        print(self.prop['correlation-id'])
        return self.prop['correlation-id']


