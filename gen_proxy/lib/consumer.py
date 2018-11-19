import pika
import json 
from Pickling import Pickling
from pprint import pprint
from publisher import FirmsPublisher
import traceback
class FirmsConsumer:
    def __init__(self, config):
        self.config = config
        self.connection=None
        self.channel=None

 
    def __enter__(self):
        self.connection = self._create_connection()
        return self
 
    def __exit__(self, *args):
        print("connection closed")
        self.channel.stop_consuming()
        self.connection.close()
 
    def consume(self, message_received_callback):
        self.message_received_callback = message_received_callback
 
        self.channel = self.connection.channel()
 
        #self.create_exchange(channel)
        #self.create_queue(channel)
 
        #channel.queue_bind(queue=self.config['queueName'],
        #                   exchange=self.config['exchangeName'],
        #                   routing_key=self.config['routingKey'])
 
        self.channel.basic_consume(self._consume_message, queue=self.config['queueName'])
        self.channel.start_consuming()
 
    def create_exchange(self, channel):
        exchange_options = self.config['exchangeOptions']
        self.channel.exchange_declare(exchange=self.config['exchangeName'],
                                 exchange_type=self.config['exchangeType'],
                                 passive=exchange_options['passive'],
                                 durable=exchange_options['durable'],
                                 auto_delete=exchange_options['autoDelete'],
                                 internal=exchange_options['internal'])
 
    def create_queue(self, channel):
        queue_options = self.config['queueOptions']
        self.channel.queue_declare(queue=self.config['queueName'],
                              passive=queue_options['passive'],
                              durable=queue_options['durable'],
                              exclusive=queue_options['exclusive'],
                              auto_delete=queue_options['autoDelete'])
 
    def _create_connection(self):
        credentials = pika.PlainCredentials(self.config['userName'], self.config['password'])
        parameters = pika.ConnectionParameters(self.config['host'], self.config['port'],
                                               self.config['virtualHost'], credentials, ssl=False)
        return pika.BlockingConnection(parameters)
 
    def _consume_message(self, channel, method, properties, body):
        #print(method.consumer_tag)
        #print(properties.headers)
        properties=properties.headers
        body=json.loads(body)
        try:
            res= self.message_received_callback(properties,body)
        except Exception as e:
            raise 
            print("Handler received exception {} ".format(e))
            res=None
        if res:
            self.channel.basic_ack(delivery_tag=method.delivery_tag)
        else:
            self.channel.basic_nack(delivery_tag=method.delivery_tag)

class WorkFlowMonitor:
    def __init__(self):
        self.config={'userName':'kannan',
            'password':'divya123',
            'host':'rabbitmq-1',
            'port':'5672',
            'virtualHost':'/',
            'exchangeName':'work_flow_monitor_exchange',
            'routingKey':'monitor'
            }
    def update(self,msg):
         with FirmsPublisher(self.config) as  workFlowUpdateObject:
             result=workFlowUpdateObject.publish(msg)
             return result


def func(body):
    print(body)
    return 1


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

        



class DataStore:
    def __init__(self,prop,msg):
        self.prop=prop.headers
        self.msg=msg
        self.pickle=Pickling("gen_proxy_db")
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
                #print(data)
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



