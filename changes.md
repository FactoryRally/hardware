# Eventhandling

Currently only the `MovementEvent` has a default handler which prints out the message. The other Eventtypes are planned to be implemented.

## Other Eventtypes

New Eventtypes should be added to the `RELEVANT_ACTIONS` list in `MQTT_Publisher`. If an event is of one of this types, it will be sent to the according subscriber aka robot.
For a robot to actually perform this action, it needs to have a method, which evaluates the given message and convert it to a concrete call. 
An example for this behavior is:

```
...
msg_decoded = dict(msg)
if event_type == "MovementEvent":
    print(f"perform_movement({msg_decoded.get('entity')}, {msg_decoded.get('direction')}, "
          f"{msg_decoded.get('rotation')}, {msg_decoded.get('rotation-times')}, {msg_decoded.get('to').get('x')},"
          f" {msg_decoded.get('to').get('y')}")
```

# Game Scan

Currently there is no Game scan due to the usage of the `simple_api_rest` library. This is a comfort change which should be added in the future.

# Terminal output

Currently there is no terminal output, which explains what needs to be done now. This should be easily achieveable through change the service.
