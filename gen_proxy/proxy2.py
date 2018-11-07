from lib.consumer import FirmsConsumer
from lib.publisher import FirmsPublisher
from lib.data_store import DataStore
from lib.work_flow_update import WorkFlowMonitor
import traceback

def callback(prop,msg):
    print(prop,msg)
    log_message={}
    log_message["headers"]=prop.headers
    log_message["Payload"]=msg
    Data=DataStore(prop,msg).process()
    if Data:
        if isinstance(Data,bool):
            return Data
        else:
          print("In call back ")
          publisher_config={'userName':'kannan',
            'password':'divya123',
            'host':'rabbitmq-1',
            'port':'5672',
            'virtualHost':'/',
            'exchangeName':'gen_proxy_exchange',
            'routingKey':'gen'
            }
        with FirmsPublisher(publisher_config) as  generateInstance:
            result=generateInstance.publish(Data)
        if result:
            result2=WorkFlowMonitor().update(log_message)
            print("message to be published is -->{}".format(log_message))
            if result2:
                print("Message is updated to work flow monitor")
            return True
    else:
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

