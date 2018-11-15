import json
import time
import traceback
from multiprocessing import Lock, Process, current_process

from data_store import DataStore


# fixme - Remind to gather all the the remaining messages
# FIXME - Should I be using Multiprocessing
class Aggreagator:
    """  doc """
    
    def __init__(self, validatormsg):
        self.msg = validatormsg
        self.datastore = DataStore("test.db")
    
    @property
    def verifymsg(self):
        """ doc """
        try:
            assert isinstance(self.msg, dict)
            assert "header" in self.msg and len(self.msg["header"]) > 0
            assert "payload" in self.msg and len(self.msg["payload"]) > 0
        except AssertionError:
            print("verify msg failed")
            raise
            return False
        return True
    
    def get_header_payload(self):
        return (self.msg["header"], self.msg["payload"])
    
    def verify_if_message_in_queue(self, corrid, tablename):
        query_str = "select * from {} where correlation_id=:1".format(tablename)
        # ret=self.datastore.select_data("select * from validator where correlation_id=:1",(corrid,))
        ret = self.datastore.select_data(query_str, (corrid,))
        # print(ret)
        return (len(ret), ret)
    
    def process_validator_msg(self, lock):
        print(current_process().name)
        if not self.verifymsg:
            return False
        (header, payload) = self.get_header_payload()
        ret, _ = self.verify_if_message_in_queue(header["correlation_id"], "validator")
        if not ret:
            try:
                self.datastore.insert("insert into validator values (?,?,?,?,?,?,?)", [None,
                                                                                       str(time.time()),
                                                                                       header["correlation_id"],
                                                                                       header["username"],
                                                                                       header["ticket_num"],
                                                                                       header["type"],
                                                                                       json.dumps(payload)
                                                                                       ])
            
            except:
                errorStack = traceback.format_exc()
                print(errorStack.split('\n'))
                # print('ERROR ' + errorStack.split('\n')[-2])
                return False
        else:
            print("Message already exist in the table")
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
        if not self.verifymsg:
            return False
        print(current_process().name)
        ret_reqUpdator_upd = False
        ret_validator_upd = False
        final_msg = None
        (header, payload) = self.get_header_payload()
        
        ret_reqUpdator_upd = self.insert_request_update_table(header, payload)
        if ret_reqUpdator_upd:
            print("message from Requester updated is inserted into the table")
            ret_validator_upd, data = self.verify_if_message_in_queue(header["correlation_id"], "validator")
            
            if ret_validator_upd:
                if ret_validator_upd == 1:
                    print("message in validator queue we can proceed")
                    final_msg = self.get_final_msg(data)
                    return (ret_validator_upd, ret_reqUpdator_upd, final_msg)
                    print(final_msg)
                elif ret_validator_upd > 1:
                    print("more than 1 message for correlation id {}".format(header["correlation_id"]))
                    final_msg = self.get_final_msg(data)
                    return (ret_validator_upd, ret_reqUpdator_upd, final_msg)
            
            else:
                print("""message not in validator queue for the corresponaing message received from request upater""")
                return (ret_validator_upd, ret_reqUpdator_upd)
        else:
            print("Request updater msg insert failed")
            return (ret_validator_upd, ret_reqUpdator_upd)
        return (ret_validator_upd, ret_reqUpdator_upd)
        # FIXME - does it have to return a tuple of BOOLEAN or just a BOOLEAN
    
    def insert_request_update_table(self, header, payload):
        try:
            self.datastore.insert("insert into requester_updater values (?,?,?,?,?,?,?,?)", [None,
                                                                                             str(time.time()),
                                                                                             header["correlation_id"],
                                                                                             header["username"],
                                                                                             header["ticket_num"],
                                                                                             header["type"],
                                                                                             header["status"],
                                                                                             json.dumps(payload)
                                                                                             ])
        except Exception as e:
            print(e)
            return False
        return True
    
    def get_final_msg(self, data):
        _msg = data[0][0]
        _final_msg = {}
        _header = {}
        _header["correlation_id"] = _msg[2]
        _header["username"] = _msg[3]
        _header["ticket_num"] = _msg[4]
        _header["type"] = _msg[5]
        payload = json.loads(_msg[6])
        _final_msg["header"] = _header
        _final_msg["payload"] = payload
        return _final_msg
    
    def CheckingQueueForMessage(self):
        # fixme - write logic for looking each message in the Queue
        pass
    
    def get_status_of_db(self):
        # fixme - write logic for checking if db is available (and same to be written in datastore)
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
            "correlation_id": "1111zzz",
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
            "correlation_id": "111199",
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
    
    # ag=Aggreagator(msg3)
    # ret=ag.process_validator_msg()
    # ret=ag.verify_if_message_in_queue("11117","validator")
    # ret=ag.process_requestupdater_msg()
    # print(ret)
    
    msg4 = {}
    obj1 = Aggreagator(msg2)
    obj2 = Aggreagator(msg3)
    lock = Lock()
    p1 = Process(target=obj1.process_validator_msg, args=(lock,))
    p2 = Process(target=obj2.process_requestupdater_msg, args=(lock,))
    p2.start()
    p1.start()
    p1.join()
    p2.join()
