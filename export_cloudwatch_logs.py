import boto3
import datetime
import time
import pandas as pd
import sys
import traceback
import yaml

def init_config():
    with open("config.yml", 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
        return config

def get_from_time(config):
    if 'from_time' in config['cloudwatch_log_export']:
        return datetime.datetime.strptime(config['cloudwatch_log_export']['from_time'], '%Y/%m/%d %H:%M:%S %Z')

def get_to_time(config):
    if 'to_time' in config['cloudwatch_log_export']:
        return datetime.datetime.strptime(config['cloudwatch_log_export']['to_time'], '%Y/%m/%d %H:%M:%S %Z')

def export_cloudwatch_logs_to_s3():
    config = init_config()
    client = boto3.client('logs',
                aws_access_key_id=config['aws']['aws_access_key_id'],
                aws_secret_access_key=config['aws']['aws_secret_access_key'],
                region_name=config['aws']['region_name']
            )
    from_time = get_from_time(config)
    to_time = get_to_time(config)
    from_time_int = int(from_time.timestamp())
    to_time_int = int(to_time.timestamp())

    intervals = pd.date_range(from_time, to_time, freq='MS')
    log_groups = config['cloudwatch_log_export']['log_groups']
    for log_group in log_groups:
        for i in range(0, len(intervals) - 1):
            destination_prefix = f"{log_group[1:]}/{intervals[i].strftime('%Y-%m-%d')}_{intervals[i+1].strftime('%Y-%m-%d')}"
            print(f'Exporting {log_group} from {intervals[i]} to {intervals[i+1]} as {destination_prefix}')
            try:
                export_response = client.create_export_task(
                    taskName='export-task1',
                    logGroupName=log_group,
                    fromTime=int(intervals[i].value/1000000),
                    to=int(intervals[i+1].value/1000000),
                    destination=config['cloudwatch_log_export']['destination_bucket'],
                    destinationPrefix=destination_prefix
                )

                describe_response = client.describe_export_tasks(
                    taskId=export_response['taskId']
                )

                status_code = describe_response['exportTasks'][0]['status']['code']
                log_group_name = describe_response['exportTasks'][0]['logGroupName']
                while status_code == 'RUNNING' or status_code == 'PENDING':
                    print(f'{log_group_name} status: {status_code}')
                    time.sleep(5)
                    describe_response = client.describe_export_tasks(
                        taskId=export_response['taskId']
                    )
                    status_code = describe_response['exportTasks'][0]['status']['code']
                print(f'{log_group_name} status: {status_code}')
            except Exception as err:
                print(err)
                traceback.print_exc()
                sys.exit()

if __name__ == '__main__':
    export_cloudwatch_logs_to_s3()