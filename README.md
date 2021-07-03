# AWS Route53 IP Monitor/Update
Updates configured Route53 entry when current external IP does not match the returned value.

## Overview
Script was originally developed due to the increased frequency with residential ISP dynamic external IPs. While there are services commercial for this (i.e. DynDNS) as well as some other open source projects, this project was written as a practical leaning experience with the boto3 library and the AWS SDK.  The current deployment method is via crontab but the project can also be ran manually, via other automation platforms or in combination with monitoring/alerting infrastructures like Zabbix or Nagios.

## Possible Use Cases
- Handle dynamic ISP external IP changes
- Update external records when switching to a different ISP (i.e. during a failover instance)
- Provide a current DNS entry when mobile (for testing or when using certain VPN services)

## Components
**aws-ipmonitor.py** - main program

**config.yml** - Configuration parameters as needed by aws-ipmonitor.py

**requirements.txt** - standard Python requirements list

## Installation: Crontab *(recommended)*
1. Clone repo to local system and move all files to desired folder location
2. Create Python virtual environment
3. Pip install using requirements.txt
3. Create crontab entry to execute the script as needed

## Crontab Resources
**Entry Syntax**

*Minute Hour DayOfMonth Month DayofWeek Command*

**Execute every day at the top of the hour**
```
0 * * * * /usr/src/aws-ipmonitor/env/bin/python /usr/src/aws-ipmonitor/aws-ipmonitor.py
```
**Execute every day at 3am**
```
0 3 * * * /usr/src/aws-ipmonitor/env/bin/python /usr/src/aws-ipmonitor/aws-ipmonitor.py
```
This is an excellent rundown of the variations for crontab entries can be found at [Codementor.io](https://www.codementor.io/@akul08/the-ultimate-crontab-cheatsheet-5op0f7o4r)

*Note: the above examples use ```$(which python3)``` to gather the python3 installation location on the individual system.  This can be omitted if a ```chmod +x aws-ipmonitor.py``` is ran to make the file executable as well as adding a shebang ```#!/usr/bin/python3``` to aws-ipmontior.py.*

## Roadmap
[ ] Email/push notifications when a record is updated

[ ] Handling of multiple IP records within the same task

[ ] Deployment guide for running via Docker/Podman container




