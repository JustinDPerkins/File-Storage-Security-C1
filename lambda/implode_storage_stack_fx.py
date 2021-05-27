import logging
import json
import urllib3
import time
import os
import boto3
from botocore.exceptions import ClientError
http = urllib3.PoolManager()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info("Logging setup Complete")
fss_key = os.environ['WS_API']
get_url = "https://cloudone.trendmicro.com/api/filestorage/external-id"
post_url = "https://cloudone.trendmicro.com/api/filestorage/stacks"
delete_url = "https://cloudone.trendmicro.com/api/filestorage/stacks/"

def lambda_handler(event, context):  
    #gather bucket name from event
    bucket_name = event['detail']['requestParameters']['bucketName']
    logger.info("s3 Bucket: " + bucket_name)
    
    # gather cloud one ext id
    r = http.request(
        "GET",
        get_url,
        headers={
            "Content-Type": "application/json",
            "api-secret-key": fss_key,
            "Api-Version": "v1",
          },
      )
    ext = json.loads(r.data.decode("utf-8"))
    ext_id = ext["externalID"]
    logger.info("CloudOne ExtID: " + ext_id)
    
    # gather aws account ID
    account_id = event["account"]
    logger.info("AWS account ID: " + account_id)
    
    #gather stack id
    id_call = http.request('GET', post_url, headers = {'Content-Type': 'application/json', 'api-secret-key': fss_key, 'Api-Version': 'v1'})
    id_resp = json.loads(id_call.data.decode('utf-8'))
    for data in id_resp['stacks']:
        if 'storage' in data and data['storage'] is not None:
            if bucket_name == data['storage']:
                 stack_name = data['name']
                 stack_id = data['stackID']
                 logger.info(stack_name)
                 logger.info(stack_id)
                 stack_removal(fss_key, stack_id,stack_name)
                
def stack_removal(fss_key, stack_id, stack_name):
    #delete cft stack
    cft_client = boto3.client("cloudformation")
    response = cft_client.delete_stack(StackName=stack_name)
    #delete stack from c1-fss
    id_call = http.request('DELETE', delete_url+stack_id, headers = {'Content-Type': 'application/json', 'api-secret-key': fss_key, 'Api-Version': 'v1'})
    