import pika 




class CreateQueueExchange:
   def __init__(self,config):
       self.config=config
       self.connection=None
       self.channel=None
  

   def __enter__(self):
        self.connection = self._create_connection()
        return self

   def __exit__(self, *args):
        print("connection closed")
        self.connection.close()




   def _create_connection(self):
        self.credentials = pika.PlainCredentials(self.config['userName'], self.config['password'])
        self.parameters = pika.ConnectionParameters(self.config['host'], self.config['port'],
                                               self.config['virtualHost'], self.credentials, ssl=False)
        return pika.BlockingConnection(self.parameters)


   def _create_exchange(self, channel):
        exchange_options = self.config['exchangeOptions']
        self.channel.exchange_declare(exchange=self.config['exchangeName'],
                                 exchange_type=self.config['exchangeType'],
                                 passive=exchange_options['passive'],
                                 durable=exchange_options['durable'],
                                 auto_delete=exchange_options['autoDelete'],
                                 internal=exchange_options['internal'])

   def _create_queue(self, channel):
        queue_options = self.config['queueOptions']
        self.channel.queue_declare(queue=self.config['queueName'],
                              passive=queue_options['passive'],
                              durable=queue_options['durable'],
                              exclusive=queue_options['exclusive'],
                              auto_delete=queue_options['autoDelete'])
   
   def create(self):
        self.channel=self.connection.channel()
        self._create_exchange(self.channel)
        self._create_queue(self.channel)
        self.channel.queue_bind(queue=self.config['queueName'],
                           exchange=self.config['exchangeName'],
                           routing_key=self.config['routingKey'])

  

config={'userName':'kannan',
        'password':'divya123',
        'host':'rabbitmq-2',
        'port':'5672',
        'virtualHost':'/',
        'exchangeName':'divi',
        'exchangeType':'topic',
        'exchangeOptions':{'passive':False,'durable':True,'autoDelete':False,'internal':False},
        'queueOptions':{'passive':False,'durable':True,'exclusive':False,'autoDelete':False},
        'queueName':'divi1',
        'routingKey':'divi.#',
        'props':{'content_type' :'text/plain',
                 'delivery_mode':2}
        }




with CreateQueueExchange(config) as client:
    client.create()
