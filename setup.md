# Installation

The Hardware-Interface is designed to be installed on a Raspberry Pi with WIFI module, however it basically is compatible with any Linux distro with Python3.

If Python3 is not installed, it can be by using:

```
sudo apt install python3
```

If everything needed is installed, activate the venv and run the application.

```
source env/bin/activate
python3 -m pip install -r requirements.txt
python3 Hardware_main.py
```

*Currently there is no service which runs the application due to issues with networking.*
