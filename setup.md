# Installation

The Hardware-Interface is designed to be installed on a Raspberry Pi with WIFI module, however it basically is compatible with any Linux distro with `nmcli` und Python3.

If either `nmcli` or Python3 are not installed, they can be by using:

```
sudo apt-get install network-manager
sudo apt install python3
```

If everything needed is installed, activate the venv and run the application.

```
source env/bin/activate
python3 Hardware_main.py
```

## Own Raspberry Pis

On the default Raspberry Pi from us, the application is starting on boot, this can be enabled on any device through by adding the following line at the bottom of `/etc/profile`. 

```
sudo python3 /path/to/file.py
```
