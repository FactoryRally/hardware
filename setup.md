# Installation

## MQTT-Publisher

The Hardware-Interface is designed to be installed on a Raspberry Pi with WIFI module, however it basically is compatible with any Linux distro with Python3.

If Python3 is not installed, it can be by using:

```
sudo apt install python3
```

If everything needed is installed, activate the venv and run the application.

```
source env/bin/activate
python3 -m pip install -r requirements.txt
```

*Currently there is no service which runs the application due to issues with networking.*

It should be able to define a service, which however is not displaying text output yet.

First you need to create a sh-script, which only executes the Python-script `Hardware_Main.py`.

```
touch FactoryRally.sh
chmod u+x FactoryRally.sh
echo "python3 FactoryRally.sh"
```

Now you need to create a service, which runs after a WIFI connection is established.

```
sudo systemctl edit --force --full FactoryRally.service
```

Insert this and change the path to your sh-Script accordingly.


```
[Unit]
Description=My Script Service
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi
ExecStart=/home/pi/FactoyRally.sh

[Install]
WantedBy=multi-user.target
```



Now enable and start the service, so with the next restart it should run correct.

```
sudo systemctl enable FactoyRally.service
sudo systemctl start FactoyRally.service
```

Now you need to create a service, which runs after a WIFI connection is established.

## MQTT-Subscriber

The subscriber has a similiar structure. So you need to change into the directory and

```
source env/bin/activate
python3 -m pip install -r requirements.txt
```
