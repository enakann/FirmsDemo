loop:
    consume_from_queue()
        store_consumed_message_in_local_store()
        call_processor_with_message()
        delete_processed_message()
	
aggregator --exchange

validator -valid  validator_consumer.py  validator_publisher.py

requpdater -req  request_updater_consumer.py  requpdated_publisher.py



					   
msg={"Message_header":                      
{
    "username":"navi",
    "ticket-num":"srno1",
    "correlation-id":11110
},
"Payload":
{
    "source":"10.10.10.1",
    "destination":"10.172.2.1",
    "port": 22,
    "protocol":"tcp",
    "input-row-id" :1
}}


method.consumer_tag
###################
request_validater:ctag1.a3949082830e402e8bcf69ee66a231d5
gen_proxy:ctag1.8ed5aade64b0455da2f403a9be0fb65a


headers:{'username': u'navi', 'ticket-num': u'srno1', 'correlation-id': 11110}
msg={"Payload": {"source": "10.10.10.1", "destination": "10.172.2.1", "protocol": "tcp", "port": 22, "input-row-id": 1}}

data_store={11110:
                 {'headers':headers,
                   'msg':msg
				   },
			11111:
                 {'headers':headers,
                   'msg':msg
				   }
			}
				 




Validator---->(proxy)-------------------------------[ gen queue ]--------------------->(generator)
               - pickled file
			   - method which listen to
          			   request updated queue
			   - publish the message to
        			   generator queue once ticket progress
					   received from request updater


how to run
##########
run in order

1.validator/publisher.py
2.gen_proxy/gen_proxy.py
