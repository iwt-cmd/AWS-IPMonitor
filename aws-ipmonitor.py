#!/usr/bin/python3
import requests
import boto3
import yaml
import logging
from datetime import datetime

#Retrive current Route53 IP address
def get_current_record(aws_account, aws_key, zone_id, record):
    client = boto3.client('route53', aws_access_key_id=aws_account, aws_secret_access_key=aws_key)
    current_record = client.list_resource_record_sets(HostedZoneId=zone_id, StartRecordName=record, MaxItems="1")
    return current_record['ResourceRecordSets'][0]['ResourceRecords'][0]['Value']

#Update Route53 IP address
def update_record(aws_account, aws_key, zone_id, record, record_value):
    client = boto3.client('route53', aws_access_key_id=aws_account, aws_secret_access_key=aws_key)
    change = client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={'Changes':[{'Action':'UPSERT', 'ResourceRecordSet':{'Name': record, 'Type':'A', 'TTL':300, 'ResourceRecords':[{'Value': record_value}]}}]}
    )

#Get current outside IP from AWS CheckIP service
def current_IP():
    return ((requests.get('http://checkip.amazonaws.com')).text).replace("\n", "")

if __name__ == "__main__":
    try:
        #Update path below if using different location to store config.yml.  Other file path changes are handled within config.yml
        with open("/usr/src/aws-ipmonitor/config.yml", 'r') as ymlfile:
            config = yaml.load(ymlfile, Loader=yaml.FullLoader)
    except:
        logging.warning("Config file not found")
    
    try:
        aws_account = config["creds"]["aws_account"]
        aws_key =  config["creds"]["aws_key"]
        zone_id = config["zone"]["zone_id"]
        record = config["zone"]["record"]
        record_value = current_IP()
        log_file = config["config"]["log_file"]
    except:
        logging.warning("Config file not formatted correctly or missing values")
    
    
    current_record = get_current_record(aws_account, aws_key, zone_id, record)
    if current_record != record_value:
        update_record(aws_account, aws_key, zone_id, record, record_value)
        new_record = get_current_record(aws_account, aws_key, zone_id, record)
        now = datetime.now()
        now = now.strftime("%m/%d/%y %H:%M:%S")
        with open(log_file, "a") as lf:
            lf.write(f"{now} {record} {current_record} >> {new_record}\n")