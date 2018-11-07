GENERATOR
************

TO test this run
---------------
1.python validator/publisher.py
2.python gen_proxy/gen_proxy.py
3.python generator/consumer.py



Exchane:Generator_Exchange
type:topic
queu1:
     name:proxy2_queue
	 routingkey:new.*
queue2:
      name:change_manager_queue
	  routingkey:*.policy
	  [new.policy,existing.policy,redflags.policy]

msg={
  "headers":{
    "username":"navi",
    "ticket-num":"srno123",
    "correlation-id":"12345"
     },
 "New_Policies":{
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
}
