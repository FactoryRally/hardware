# A real robot - MQTT requirements

Any subscriber implementation needs to able to register to the publisher and receive its id. Furthermore the address of the broker needs to be changed. 

Specifically, the `on_message` method must allow the ID to be received and there must be a `discover` method to register it. 

The `discover` needs to send a message on the `general` topic to the publisher.

```
elif not self.id_received and str(msg_decoded).__contains__("Your client topic is"):
    act_payload = eval(msg.payload.decode()).get('topic')
    self.topic = "client-"+act_payload
    client.subscribe(self.topic)
    print(f"subscribed to `{self.topic}`")
    self.id_received = True
```

The `on_message` handles the ID, which will be sent from the publisher. 

```
elif not self.id_received and str(msg_decoded).__contains__("Your client topic is"):
    act_payload = eval(msg.payload.decode()).get('topic')
    self.topic = "client-"+act_payload
    client.subscribe(self.topic)
    print(f"subscribed to `{self.topic}`")
    self.id_received = True
