# pigateway
Raspberry Pi gateway from Modbus RTU to cloud (influxdb). The device Modbus register map can be created using YAML file. 
Currently there are Modbus maps for ORNO OR-WE-504 and OR-WE-516 energy meters.

## Basic setup for Raspberry Pi
1. Install Raspberry Pi OS Lite to an SD card
2. Change the default password
3. Set up networking using terminal, if needed
4. Set up SSH server (using raspi-config), if needed
5. The pi should be now accessible at raspberrypi.local
6. Enable serial port hardware, disable serial port login (using sudo raspi-config)

## Setting up this gateway
1. Install GIT and Python 3 virtual environment: `sudo apt install git python3-venv`
1. Clone the repository to Raspberry: `git clone https://github.com/tuomoko/pigateway.git`
2. Create a Python virtual environment: `python3 -m venv env` This creates Python virtual environment under the folder env.
3. Activate the virtual environment: `source env/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Adjust parameters in config.py. You can use config.py.example as a template.
6. Create Modbus maps for your devices where necessary.
7. Add .crt and .key files to the keys/ folder if necessary
8. Try running the gateway `python meter_daemon.py`
9. Copy the daemon service to the systemd directory and give proper permissions: `sudo cp service/meter_daemon.service /etc/systemd/system/meter_daemon.service` and `sudo chmod 644 /etc/systemd/system/meter_daemon.service`
10. Try out the service `sudo systemctl start meter_daemon` and `sudo systemctl status meter_daemon`
11. Enable the service at bootup `sudo systemctl enable meter_daemon`


## TODO
- Implement all serial port settings in configuration file
- Implement error handling
