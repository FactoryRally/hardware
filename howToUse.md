# MQTT-Publisher

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

# MQTT-Subscriber

The Subscriber need to be started in or before `Lobby` state (later is not possible due to API restrictions). 

```
python3 MQTTReceiver.py
