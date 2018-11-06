import pika
 
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
            res= self.message_received_callback(body)
        except Exception as e:
            print("Handler received exception {} for message {}".format(e,res))
            res=None
        if res:
            self.channel.basic_ack(delivery_tag=method.delivery_tag)
        else:
            self.channel.basic_nack(delivery_tag=method.delivery_tag)



def func(body):
    print(body)
    return 1

config1={'userName':'kannan',
        'password':'divya123',
        'host':'rabbitmq-1',
        'port':'5672',
        'virtualHost':'/',
        'exchangeName':'kannan',
        'queueName':'kannan1',
        'routingKey':'kannan.log',
        'props':{'content_type' :'text/plain',
                 'delivery_mode':2}
        }

config={'userName':'kannan',
        'password':'divya123',
        'host':'rabbitmq-1',
        'port':'5672',
        'virtualHost':'/',
        'exchangeName':'validator_Exchange',
        'queueName':'request_updater',
        'routingKey':'',
        'props':{'content_type' :'text/plain',
                 'delivery_mode':2}
        }


try:
  with FirmsConsumer(config) as conn:
      conn.consume(func)
except KeyboardInterrupt:
    print("keyboard interrupt")



