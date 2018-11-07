cd Dev/

pre_process:
  run python gen_proxy/Pickling.py and check the data available

1.python gen_proxy/gen_proxy.py     -----get message from validator and store in in pickle
2.python gen/consumer_request_updater.py --- get the message from RequestUpdater/publisher.py 
                                             and remove the message from pickle and send it to generator
3.python validator/publisher.py    ----  originate the message
4.python RequestUpdater/publisher.py  ------ message sent from here will be received by consumer_request_updater.py

post_process:
   run python gen_proxy/Pickling.py check the data 
