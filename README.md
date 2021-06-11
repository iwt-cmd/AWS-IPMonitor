# AWS Route53 IP Monitor/Update
Updates configured Route53 entry when current external IP does not match the returned value.

## Overview
Script was originally developed due to the increased frequency with residential ISP dynamic external IPs. While there are services out there for this (i.e. DynDNS), this was also a pratical learning project for using the boto3 library and the AWS SDK.  The current deployment method is via a cronjob but can also be ran manually, via other automation platforms or in combination with monitoring/alerting infrastructures like Zabbix or Nagios.

## Possible Use Cases
- Handle dynamic ISP external IP changes
- Update external records when switching to a different ISP (i.e. during a failover instance)
- Provide a current DNS entry when mobile (for testing or when using certain VPN services)

## Files
**aws-ipmonitor.py** - main program

**config.yml** - Configuration paramaters as needed by aws-ipmonitor.py

**requirements.txt** - 

