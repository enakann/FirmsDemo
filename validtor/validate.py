from lib import *
import traceback
import copy
import time
from config.messages import messages
def run(config,msg):
 orig_msg=copy.deepcopy(msg)
 with FirmsPublisher(config) as  generateInstance:
            result=generateInstance.publish(msg)
            print("msg has been published ----{}".format(result))
 if result:
   print(msg)
   log_message={"headers":orig_msg["headers"],
               "Payload":{
               "time":time.time(),
                 "correlation-id":orig_msg["headers"]["correlation-id"],
                 "ticket_num":orig_msg["headers"]["ticket-num"],
                 "service_name":"validator",
                 "service_component":"validator"}}
   result2=WorkFlowMonitor().update(log_message)
   if result2:
        print("Work flow monitor is updated")
   else:
        print("Work flow monitor upate failed")





 
if __name__ == '__main__':

    config={'userName':'kannan',
            'password':'divya123',
            'host':'rabbitmq-1',
            'port':'5672',
            'virtualHost':'/',
            'exchangeName':'validator_Exchange',
            'routingKey':''
            }

    #msgs=sys.argv[1:]
    msg1={"headers":                      
    {
        "username":"navi",
        "ticket-num":"srno1",
        "correlation-id":11119
    },
    "Payload":
    {
        "source":"10.10.10.1",
        "destination":"10.172.2.1",
        "port": 22,
        "protocol":"tcp",
        "input-row-id" :1
    }}

    msg=messages.pop()


    try:
      run(config,msg)
    except Exception as e:
        traceback.print_exc()
        raise e



        
