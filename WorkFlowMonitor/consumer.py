import pika
from publisher import FirmsPublisher 
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
        print(method.consumer_tag)
        try:
            res= self.message_received_callback(properties,body)
        except Exception as e:
            print("Handler received exception {}".format(e))
            res=None
        if res:
            self.channel.basic_nack(delivery_tag=method.delivery_tag)
        else:
            self.channel.basic_nack(delivery_tag=method.delivery_tag)



def callback(*args,**kwargs):
    data=Generate(*args,**kwargs).process()
    if data:
         config={'userName':'kannan',
            'password':'divya123',
            'host':'rabbitmq-1',
            'port':'5672',
            'virtualHost':'/',
            'exchangeName':'Generator_Exchange'
            }

         with FirmsPublisher(config) as  generateInstance:
            result=generateInstance.publish(data,"new.policy")
            print("Message Published ---{}".format(result))
    return True




class Generate:
    def __init__(self,prop,msg):
        self.prop=prop.headers
        self.msg=msg
        self.correlation_id=None
        self.out_msg={}
    def process(self):
        #self.correlation_id=self.get_corrid()
         self.out_msg['headers']=self.prop
         self.out_msg['new_policy']=self.get_new_policy()
         return self.out_msg    
    def get_corrid(self):
          return self.prop['correlation-id']
    def get_new_policy(self):
        new_policy= {
        "Payload":
              {
            "firewall":{
                "meta-data":
                {
                    "vendor":"Cisco",
                    "model":"SRX",
                },
                "cmds":
                [
                    "new_src_cmd",
                    "new_dst_cmd",
                    "new_app_cmd",
                    "pol_no",
                ]
                }
             }
	   }
         
        return new_policy

    def get_existing_policy(self):
        existing_policy={
                "Payload":
            {
                "firewall":"firewall",
                "policy-name":"policy-name",
                "source-ip":"source-ip",
                "destination-ip":"destination-ip",
                "port":"port",
                "input-row-id":"input-row-id"
            }
         }
        return existing_policy
    def get_red_flags(self):
        red_flag= {
                "Source-IP": "Source-IP",
                "Routing-Issue-Reason":"Routing-Issue-Reason",
                "Input-Row-ID":"Input-Row-ID",
                "Destination-Firewall":"Destination-Firewall",
                "Dest-Zone-2":"Dest-Zone-2",           
                "Source-Zone":"Source-Zone",
                "Dest-Zone":"Dest-Zone",
                "Destination-IP":"Destination-IP",
                "Source-Zone-2":"Source-Zone-2",
                "Source-Firewall":"Source-Firewall",
                "Port": "Port"
             }
        return red_flags








def func(properties,body):
    print(properties.headers)
    print(body)
    return 1


config={'userName':'kannan',
        'password':'divya123',
        'host':'rabbitmq-1',
        'port':'5672',
        'virtualHost':'/',
        'exchangeName':'work_flow_monitor_exchange',
        'queueName':'work_flow_monitor_queue',
        'routingKey':'monitor',
        'props':{'content_type' :'text/plain',
                 'delivery_mode':2}
        }


try:
  with FirmsConsumer(config) as conn:
      conn.consume(func)
except KeyboardInterrupt:
    print("keyboard interrupt")



