from multiprocessing import Process
from gen_proxy import FirmsConsumer,callback



def consume_process(config):
 try:
   with FirmsConsumer(config) as conn:
      conn.consume(callback)
 except KeyboardInterrupt:
     print("keyboard interrupt")
 except Exception as e:
    traceback.print_exc()
    raise 

		
if __name__ == '__main__':
    
    config_cm={'userName':'kannan',
    'password':'divya123',
    'host':'rabbitmq-1',
    'port':'5672',
    'virtualHost':'/',
    'exchangeName':'requester_updater_exchange',
    'queueName':'proxy1',
    'routingKey':'',
    'props':{'content_type' :'text/plain',
             'delivery_mode':2}
    }
	
	
	
    consumer_list = []
    consumer_list.append(config_cm)
# execute
    process_list = []
    for sub in consumer_list:
        process = Process(target=consume_process,args=(config_cm,))
        process.start()
        process_list.append(process)
# wait for all process to finish
    for process in process_list:
        process.join()



