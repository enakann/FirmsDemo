import json
import time
import traceback
from multiprocessing import Lock, Process, current_process
from time import sleep

from data_store import DataStore


class AggregatorException(Exception):
    
    pass
#try:
#		1/0
#	except Exception:
#		exc_class, exc, traceback = sys.exc_info()
#                my_exc = AggregatorException('Caching error: %s' % exc)
#                raise my_exc.__class__, my_exc, traceback

##################################################################################

#def func():
#    try:
#        raise ValueError ("couldnt find", "a")
#    except Exception:
#        exc_class, exc, traceback = sys.exc_info ()
#        print (exc)
#        my_exc = StuffCachingError ('Caching error: %s' % exc)
#        raise my_exc.__class__, my_exc, traceback

#>> > func ()
#('couldnt find', 'a')
#Traceback (most recent call last):
#File "<pyshell#169>", line 1, in < module >
#func ()
#File "<pyshell#168>", line 3, in func
#raise ValueError ("couldnt find", "a")
#StuffCachingError: Caching
#error: ('couldnt find', 'a')

####################################################################################


# fixme - Remind to gather all the the remaining messages
# FIXME - Should I be using Multiprocessing

class Aggreagator:
    """  doc """

    def __init__(self, workflow_monitor,validatormsg):
        self.workflow_monitor=workflow_monitor
        self.msg = validatormsg
        self.db = "test.db"
    
    @property
    def verifymsg(self):
        """ doc """
        try:
            return all ([isinstance (self.msg, dict),
                         "header" in self.msg and len (self.msg["header"]) > 0,
                         "payload" in self.msg and len (self.msg["payload"]) > 0
                         ])
        
        except Exception as e:
            print ("verify msg failed".format (e))
        return False
    
    def get_header_payload(self):
        return self.msg["header"], self.msg["payload"]
    
    def get_msg_from_validator_table(self, corrid, tablename):
        query_str = "select * from {} where correlation_id=:1".format (tablename)
        with DataStore(self.db) as dbobj:
            ret = dbobj.select_data (query_str, (corrid,))
            return ret
    
    def process_validator_msg(self, lock):
        if not self.verifymsg:
            return False
        
        (header, payload) = self.get_header_payload ()
        ret = self.get_msg_from_validator_table (header["correlation_id"], "validator")
        if not ret:
            try:
                with DataStore(self.db) as dbobj:
                    dbobj.insert("insert into validator values (?,?,?,?,?,?,?)",[None,
                                                                                str(time.time ()),
                                                                                header["correlation_id"],
                                                                                header["username"],
                                                                                header["ticket_num"],
                                                                                header["type"],
                                                                                json.dumps (payload)
                                                                                ])
            
            except:
                errorstack = traceback.format_exc ()
                print (errorstack.split ('\n'))
                # print('ERROR ' + errorStack.split('\n')[-2])
                return False
        else:
            print ("Message already exist in the table")
            # FIXME - may be we have to delete the old message and insert the new one
            return False
    
    def process_requestupdater_msg(self, lock):
        """
        ret_validator_upd:status of the validator func
        ret_reqUpdator_upd: status of request updater
        (1, True)=self.process_requestupdater_msg()
        1=
        :return:
        """

        req_updtr_ret = False
        final_msg = dict()
        try:
            if not self.verifymsg:
                return req_updtr_ret,final_msg
            
            (header, payload) = self.get_header_payload()
    
            req_updtr_ret = self.insert_request_update_table(header, payload)
    
            if req_updtr_ret:
                print ("message from Requester updated is inserted into the table")
                data = self.get_msg_from_validator_table (header["correlation_id"], "validator")
                print(data)
                if data:
                    print ("message in validator queue we can proceed")
                    final_msg = self.get_final_msg (data[0])
                    return req_updtr_ret, final_msg
                else:
                    print ("message not in validator queue for the corresponaing message received from request upater""")
                    return req_updtr_ret, final_msg
            else:
                print ("Request updater msg insert failed")
                return req_updtr_ret, final_msg
        except Exception as e:
            print(e)
            return req_updtr_ret,final_msg
            
        # FIXME - does it have to return a tuple of BOOLEAN or just a BOOLEAN
    
    def insert_request_update_table(self, header, payload):
        try:
            with DataStore (self.db) as dbobj:
                dbobj.insert("insert into requester_updater values (?,?,?,?,?,?,?,?)", [None,
                                                                                        str (time.time ()),
                                                                                        header["correlation_id"],
                                                                                        header["username"],
                                                                                        header["ticket_num"],
                                                                                        header["type"],
                                                                                        header["status"],
                                                                                        json.dumps (payload)
                                                                                        ])
            return True
        except Exception as e:
            print(e)
            return False
        
    def verify_msg_from_requpdater_table(self,msg):
        """ [(8, 1542392569.829502, '1111aa', 'navi', 'srno2', 'validator',
        '{"source": "10.10.10.3", "destination": "10.172.2.3", "port": 22, "protocol": "tcp", "input-row-id": 1}')]"""
        
        
       
        
    
    def get_final_msg(self, data):
        _msg = data
        _final_msg = dict()
        _header = dict()
        _header["correlation_id"] = _msg[2]
        _header["username"] = _msg[3]
        _header["ticket_num"] = _msg[4]
        _header["type"] = _msg[5]
        
        _payload = json.loads(_msg[6])
        
        _final_msg["header"] = _header
        _final_msg["payload"] = _payload
        
        return _final_msg
    
    def delete_msg(self,table,corrid):
        query_str="delete from {} where correlation_id=:1".format(table)
        print(query_str)
        with DataStore (self.db) as dbobj:
            ret = dbobj.delete(query_str, (corrid,))
            return ret
        
    
    def CheckingQueueForMessage(self):
        # fixme - write logic for looking each message in the Queue
        pass
    



if __name__ == '__main__':
    msg = {"payload": {
        "source": "10.10.10.3",
        "destination": "10.172.2.3",
        "port": 22,
        "protocol": "tcp",
        "input-row-id": 1
    }}
    
    msg2 = {
        "header": {
            "username": "navi",
            "ticket_num": "srno2",
            "correlation_id": "1111aa",
            "type": "validator"
        },
        "payload": {
            "source": "10.10.10.3",
            "destination": "10.172.2.3",
            "port": 22,
            "protocol": "tcp",
            "input-row-id": 1
        }}
    
    msg3 = {
        "header": {
            "username": "navi",
            "ticket_num": "srno2",
            "correlation_id": "1111aa",
            "type": "validator",
            "status": "Progress"
        },
        "payload": {
            "source": "10.10.10.3",
            "destination": "10.172.2.3",
            "port": 22,
            "protocol": "tcp",
            "input-row-id": 1
        }}
    
    #ag=Aggreagator("test",msg3)
    #ret=ag.delete_msg("validator",111199)
    #print(ret)
    # ret=ag.process_validator_msg()
    # ret=ag.get_msg_from_validator_table("11117","validator")
    # ret=ag.process_requestupdater_msg()
    # print(ret)
    
    #msg4 = {}
    obj1 = Aggreagator ("wfm",msg2)
    obj2 = Aggreagator ("wfm",msg3)
    lock = Lock ()
    p1 = Process (target=obj1.process_validator_msg, args=(lock,))
    sleep(2)
    p2 = Process (target=obj2.process_requestupdater_msg, args=(lock,))
    p2.start ()
    p1.start ()
    p1.join ()
    p2.join ()
