import requests
import boto3
import yaml
import logging
from datetime import datetime

def get_current_record(aws_account, aws_key, zone_id, record):
    client = boto3.client('route53', aws_access_key_id=aws_account, aws_secret_access_key=aws_key)
    current_record = client.list_resource_record_sets(HostedZoneId=zone_id, StartRecordName=record, MaxItems="1")
    return current_record['ResourceRecordSets'][0]['ResourceRecords'][0]['Value']
    
def update_record(aws_account, aws_key, zone_id, record, record_value):
    client = boto3.client('route53', aws_access_key_id=aws_account, aws_secret_access_key=aws_key)
    change = client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={'Changes':[{'Action':'UPSERT', 'ResourceRecordSet':{'Name': record, 'Type':'A', 'TTL':300, 'ResourceRecords':[{'Value': record_value}]}}]}
    )
if __name__ == "__main__":
    try:
        with open("test.yml", 'r') as ymlfile:
            config = yaml.load(ymlfile, Loader=yaml.FullLoader)
    except:
        logging.warning("Config file not found")
    
    try:
        aws_account = config["creds"]["aws_account"]
        aws_key =  config["creds"]["aws_key"]
        zone_id = config["zone"]["zone_id"]
        record = config["zone"]["record"]
        record_value = config["zone"]["record_value"]
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