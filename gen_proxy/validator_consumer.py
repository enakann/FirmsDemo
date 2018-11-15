from lib.consumer import FirmsConsumer
from lib.publisher import FirmsPublisher
from lib.data_store import DataStore
from lib.work_flow_update import WorkFlowMonitor
from aggregator import Aggreagator
import copy
import traceback


def callback(msg):
    # msg_log=copy.deepcopy(msg)
    # workflow_monitor=WorkFlowMonitor().update(log_message)
    try:
        result = Aggreagator(msg).process_validator_msg()
        if result:
            print("Succesfully updated msg into validator table")
            workflow_monitor(" msg {} is updated in aggregator".format(msg))
            return True
    except Exception as e:
        workflow_monitor(" msg {} update failed  in aggregator datastore".format(msg))
        return False
    return False







if __name__ == '__main__':

    config={'userName':'kannan',
            'password':'divya123',
            'host':'rabbitmq-1',
            'port':'5672',
            'virtualHost':'/',
            'exchangeName':'validator_Exchange',
            'queueName':'gen_proxy',
            'routingKey':'',
            'props':{'content_type' :'text/plain',
                     'delivery_mode':2}
            }

    #import pdb;pdb.set_trace()

    try:
       with FirmsConsumer(config) as conn:
          conn.consume(callback)
    except KeyboardInterrupt:
        print("keyboard interrupt")
    except Exception as e:
        traceback.print_exc()
        raise e

