# MQTT-Publisher

First you have to connect to the WLAN, in which the game server is also running. 

If everything is installed, the application can be launched by

```
python3 Hardware_Main.py
```

First the IP of the Game Server needs to be entered like `xxx.xxx.xxx.xxx`, no port or anything else. 

Then a game needs to be in `LOBBY` state, so the consumer can resister. When you have chosen a game, the game can be started through the host.

# MQTT-Subscriber

The Subscriber need to be started in or before `Lobby` state (later is not possible due to API restrictions). 

```
python3 MQTTReceiver.py
