# boc-stuff
hello

## Setup 
- `git clone https://github.com/happehbunneh/boc-stuff`
- `cd boc-stuff`
- `sudo python setup.py`
- `sudo reboot`

## Console Commands
- `hym_mon.py` - starts the monitoring service 
- `hym_on.py` - switches on/off the Hymera Unit
- `server.py` - starts MaxTerm running locally
- `displaydata.py` - shows data of monitoring service currently running (if any)
- `serialdata.py` - shows rar incoming serial data


## Console/Monitoring Serivce Usage 
`hym_mon.py`

You'll be asked for the specified model number, serial number, and reason for test. Remember this as this will be used as the name for the databse correlated to the serial data. 

-Input for Model Number = 150, 200, or VOLD
-Input for Serial Number = * (whatever you wish)
-Input for Reason = *

Afterwards a detailed version of the data will be shown and refreshed every second. Please keep this running in the background.

## MaxTerm Usage
- Select the correct database and click 'Select Database'
- Leave or Change the 'Update Interval' and 'Batch Size' (update interval is the interval used to retrieve the data, batch size is how much data should be retrieved) 


How to Update Model Types:
`config.yaml` is where the model types and their variables are stored. If there has been a significant change in data structure please update the config to include a new model and its data structure.. use a similar format to this:

Please add the new structure under 'dataVariables'

`dataVariables:
  NEWVERSION:
    - VARIABLE_1
    - VARIABLE_2
    ...`
