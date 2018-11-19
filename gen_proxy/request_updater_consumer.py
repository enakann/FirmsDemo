from lib.consumer import FirmsConsumer
from lib.publisher import FirmsPublisher
from lib.data_store import DataStore
from lib.work_flow_update import WorkFlowMonitor
from aggregator import Aggreagator
import copy
import traceback

class ReqUpdater:
    def __init__(self,config,final_msg):
        self.config=config
        self.final_msg=final_msg
    def process(self):
        try:
           ret=FirmsPublisher(config).publish(final_msg)
           if ret:
               return True
        except Exception as e:
            print(e)
        return False
        
def callback(msg):
    # msg_log=copy.deepcopy(msg)
    workflow_monitor=WorkFlowMonitor()
    try:
        (ret_reqUpdator_upd, final_msg) = Aggreagator(workflow_monitor,msg).process_requestupdater_msg()
        
        if ret_reqUpdator_upd:
            print("request updater msg is updated into the aggregator datastore ")
            workflow_monitor("request updater msg is updated into the aggregator datastore".format(msg))
            try:
                if final_msg:
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


if __name__ == '__main__':
    
    config = {'userName': 'kannan',
              'password': 'divya123',
              'host': 'rabbitmq-1',
              'port': '5672',
              'virtualHost': '/',
              'exchangeName': 'validator_Exchange',
              'queueName': 'gen_proxy',
              'routingKey': '',
              'props': {'content_type': 'text/plain',
                        'delivery_mode': 2}
              }
    
    # import pdb;pdb.set_trace()
    
    try:
        with FirmsConsumer(config) as conn:
            conn.consume(callback)
    except KeyboardInterrupt:
        print("keyboard interrupt")
    except Exception as e:
        traceback.print_exc()
        raise e
