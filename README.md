# Hymera Monitoring Station
## Dataplicity Usage
Log in..
- `cd home/pi; su pi`

## Setup 
- `git clone https://github.com/happehbunneh/boc-stuff`
- `cd boc-stuff`
- `sudo python setup.py` (be aware for any prompts asking for confirmation, just type Y and press enter)
- `sudo reboot`

## Console Commands
- `console.py` - starts the monitoring service 
- `switch.py` - switches on/off the Hymera Unit
- `modules/serialMonitor.py` - displaying incoming data


## Console/Monitoring Serivce Usage 
`console.py`

You'll be asked for the specified model number, serial number, and reason for test. Remember this as this will be used as the name for the databse correlated to the serial data. 

- Input for Model Number = *
- Input for Serial Number = * 
- Input for Reason = *

Afterwards, data that is sent from the hymera will be shown on the screen, refreshed at every second. Please keep this running in the background. 

Before start, it will check if there is any service currently running, if so, it will ask whether you want to terminate the existing service and create a new one. If "yes", a new service is initialised, otherwise output from the existing service is shown on screen.

## Grafana Usage
- You can access Grafana through the dataplicity wormhole
