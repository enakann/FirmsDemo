from lib.consumer import FirmsConsumer
from lib.publisher import FirmsPublisher
from lib.data_store import DataStore
from lib.work_flow_update import WorkFlowMonitor
from aggregator import Aggreagator
import copy
import traceback

#@property
def verifymsg():
    """ doc """
    try:
        assert isinstance(self.msg, dict)
        assert "header" in self.msg and len(self.msg["header"]) > 0
        assert "payload" in self.msg and len(self.msg["payload"]) > 0
    except AssertionError:
        print("verify msg failed")
        return False
    return True


#>>> ls={u'payload': {u'source': u'10.10.10.1', u'destination': u'10.172.2.1', u'protocol': u'tcp', u'port': 22, u'input-row-id': 1}}
#>>> a={'username': u'navi', 'status': u'done', 'correlation_id': u'11115', 'ticket_num': u'srno1'}
#>>> ls.update(a)
#>>> ls
{'username': u'navi', 'status': u'done', 'correlation_id': u'11115', u'payload': {u'source': u'10.10.10.1', u'destination': u'10.172.2.1', u'protocol': u'tcp', u'port': 22, u'input-row-id': 1}, 'ticket_num': u'srno1'}

def callback(prop,msg):
    # msg_log=copy.deepcopy(msg)
    # workflow_monitor=WorkFlowMonitor().update(log_message)
    #verifymsg(prop,msg)
    #prop.update(msg)
    try:
        (ret_validator_upd, ret_reqUpdator_upd, final_msg) = Aggreagator(msg).process_requestupdater_msg()
        
        if ret_reqUpdator_upd:
            print("request updater msg is updated into the aggregator datastore ")
            workflow_monitor("request updater msg is updated into the aggregator datastore".format(msg))
            try:
                if ret_validator_upd and final_msg:
                    ret = FirmsPublisher(config).publish(final_msg)
                else:
                    print("for the message received form requpdater corresponding message not in validator queue")
            except Exception as e:
                print("sending message to generator Failed ")
                workflow_monitor(
                    "request updater msg is updated into the aggregator datastore due to {}".format(msg, e))
            finally:
                print("sending ack to the req updated queue anyway")
                return True
        else:
            return False
    except Exception as e:
        workflow_monitor(" msg {} update failed  in aggregator datastore due to {}".format(msg, e))
    return False


def func(prop,msg):
    prop.update(msg)
    print(prop)

if __name__ == '__main__':
    
    config = {'userName': 'kannan',
              'password': 'divya123',
              'host': 'rabbitmq-1',
              'port': '5672',
              'virtualHost': '/',
              'exchangeName': 'aggregator',
              'queueName': 'requpdater',
              'routingKey': '',
              'props': {'content_type': 'text/plain',
                        'delivery_mode': 2}
              }
    
    # import pdb;pdb.set_trace()
    
    try:
        with FirmsConsumer(config) as conn:
            conn.consume(func)
    except KeyboardInterrupt:
        print("keyboard interrupt")
    except Exception as e:
        traceback.print_exc()
        raise e
