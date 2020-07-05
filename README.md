# SMTP Monit

Python Asyncio App to monitor utils (CPU, RAM, HDD) and periodically sends file content

## Description

This app checks every period of time total CPU usage, total RAM usage and total HDD/SSD usage.  
If usage % is bigger than the one in configuration (config/conf.ini) it sends an email notification.  
It can sends periodically given file content.

## Example use and conf.ini explanation

#### Email configuration:
```
[email]
from=youremail@gmail.com
to=emailtosentto@gmail.com
hostname=smtp.gmail.com
port=465
use_tls=True
username=youremail@gmail.com
password=yoursecretpassword
```
Email configuration is self explaining, but the password should be in base64 encoding:
- your password is '53cr3t', then its base64 is 'NTNjcjN0'

For gmail, please be sure you set the account right(enable insecure apps and Forwarding POP/IMAP)

#### Monitoring parameters:
```
[monit_params]
machine_name=yourservername
pause_between_alarm=600
utils_to_monit=cpu disk memory
checking_interval=1
intervals_avg_load=60
cpu=80
disk=80
memory=80
```
Parameters explanation:
- machine_name:
    - your server name
    - will be in title of an email message
    - should be descriptive
- pause_between_alarm:
    - time in seconds between you get another ALARM when threshold exceeded is still over set level
- utils_to_monit:
    - string with space as separator
    - utils you want to monit
- checking_interval:
    - time interval in seconds
    - each interval utils are checked
- intervals_avg_load:
    - number of intervals: integer
    - when checking_interval=1 and intervals_avg_load=60, then average load will be calculated for 60s
- utils to monit:
    - cpu, percentage usage threshold
    - disk, percentage usage threshold
    - memory, percentage usage threshold
    - if util was given in ```utils_to_monit```, the threshold must be defined

#### Periodics configuration:
```
[periodics]
update_log=/var/log/updateupgrade.log 86400
```
It will send content on updateupgrade.log file every 86400 seconds, with the name in title of an email message.

Example usage:  
You want to get everyday some log files to your email. 

## Installation and running
You need to install Python.  
I wrote a help script for that (should be ok for debian based distros).
```
git clone https://github.com/marcinwrobel1986/smtp-monit.git
cd smtp-monit/
sudo chmod 777 python_install_ubu.sh
./python_install_ubu.sh
pipenv install
```
You can then run app in the background and close terminal
```
pipenv shell
nohup python3.8 main.py > /dev/null 2>&1 &
```

## TO DO:
- Tests 

## Licence and credits

Repository goes with MIT licence.
Thanks to vd2org as this  repository https://github.com/vd2org/periodic is used for periodic tasks.