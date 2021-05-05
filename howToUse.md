# MQTT-Publisher

## MQTT-Broker

In general there are two possibilities for MQTT-Broker:
1. online brokers -> just change the `broker` attribute in the `MQTTPublisher.py` 
2. Mosquitto (installed on the delivered Pi)

Basically this is solved using the online brokers so the user doesn't need to interfere with the source code. 

## Run the application

First you have to connect to the WLAN, in which the game server is also running. 

If everything is installed, the application can be launched by

```
python3 Hardware_Main.py
```

First the IP of the Game Server needs to be selected. 

Then a game needs to be in `LOBBY` state, so the consumer can resister. When you have chosen a game, the game can be started through the host.

## Run as a Service

You can run the Python application as Service, which gets executed as soon as the Pi has an active WIFI-connection.

First you need to create a *.sh* file, which only executes the Python file.

```
python3 Hardware_Main.py
```

Now you need to create a service `sudo systemctl edit --force --full FactoryRally.service`, which contains:

```
[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi
ExecStart=/home/pi/script.sh
ExecStartPre=/bin/sh -c 'until ping -c1 google.com; do sleep 1; done;'
```
Next the service should be enabled `sudo systemctl enable my_script.service`. 

After a restart, the service should be started. 

*The service is behaving weird in some networks, as it may show no ip. In that case, just start the game from the .sh from the desktop per double-click.*

# MQTT-Subscriber

The Subscriber needs to be started in or before `Lobby` state (later is not possible due to API restrictions). 

```
python3 MQTTReceiver.py
