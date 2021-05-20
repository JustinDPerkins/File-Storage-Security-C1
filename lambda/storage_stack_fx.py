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
fss_key = os.environ['C1_API']
queue_name = os.environ['SQS_Name']
stack_id = os.environ['STACK_ID']
get_url = "https://cloudone.trendmicro.com/api/filestorage/external-id"
post_url = "https://cloudone.trendmicro.com/api/filestorage/stacks"

def lambda_handler(event, context):
    #gather bucket name from event
    bucket_name = event['detail']['requestParameters']['bucketName']
    # filter event to bucket name
    substring = "copyzipsdestbucket"
    logger.info("s3 Bucket: " + bucket_name)
    if substring in bucket_name:
        print('Name matched filter:' + bucket_name)
        return 0
    else:
        #gather cloud one ext id
        r = http.request('GET', get_url, headers = {'Content-Type': 'application/json', 'api-secret-key': fss_key, 'Api-Version': 'v1'})
        ext = json.loads(r.data.decode('utf-8'))
        ext_id = ext['externalID']
        logger.info("CloudOne ExtID :" + ext_id)
        #gather aws account ID
        account_id = event['account']
        logger.info("AWS account ID: " + account_id)
        s3_client = boto3.client('s3')
        #check if encryption exsists on bucket
        try:
            response = s3_client.get_bucket_encryption(Bucket=bucket_name)
            kms_arn= response['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['KMSMasterKeyID']
            logger.info("Key Arn: " + kms_arn)
        except ClientError:
            logger.info("S3 :" + bucket_name + " has no encryption enabled")
            kms_arn = ''
        #check bucket tags
        try:
            response = s3_client.get_bucket_tagging(Bucket=bucket_name)
            tags = response['TagSet']
            tag_status=tags
        except ClientError:
            no_tags='does not have tags'
            tag_status=no_tags
        if tag_status == 'does not have tags':
            addTag(s3_client, bucket_name)
            add_storage(bucket_name, ext_id, account_id, kms_arn)
        else:
            for tags in tag_status:
                if tags['Key'] == "FSSMonitored":
                    if (tags["Value"] == 'No') or (tags["Value"] == 'no') or (tags["Value"] == 'NO'):
                        #if tag FSSMonitored is no; quit
                        logger.info("S3 :" + bucket_name + " has tag FSSMonitored == no; aborting")
                        return 0
                    elif (tags["Value"] != 'yes') or (tags["Value"] != 'Yes') or (tags["Value"] != 'YES'):
                        addTag(s3_client, bucket_name)
                        add_storage(bucket_name, ext_id, account_id, kms_arn)
                        break
            addTag(s3_client, bucket_name)

def addTag(s3_client, bucket_name):
    logger.info("Bucket: " + bucket_name + " has no tags; adding")
    response = s3_client.put_bucket_tagging(Bucket=bucket_name,
                Tagging={
                    'TagSet': [
                        {
                            'Key': 'FSSMonitored',
                            'Value': 'Yes' 
                        },
                    ]
                },
            )


def add_storage(bucket_name, ext_id, account_id, kms_arn):
    #deploy storage stack
    ExternalID = {'ParameterKey':'ExternalID', 'ParameterValue':ext_id }
    S3BucketToScan = {'ParameterKey':'S3BucketToScan', 'ParameterValue':bucket_name }
    Trigger_with_event = {'ParameterKey':'TriggerWithObjectCreatedEvent', 'ParameterValue':'true' }
    scanner_queue_url = {'ParameterKey':'ScannerSQSURL', 'ParameterValue':queue_name }
    scanner_aws_account = {'ParameterKey':'ScannerAWSAccount', 'ParameterValue':account_id }
    S3_Encryption = {'ParameterKey':'KMSKeyARNForBucketSSE', 'ParameterValue':kms_arn }
    cft_client = boto3.client('cloudformation')
    print('creating stack ..')
    cft_client.create_stack(
        StackName="C1-FSS-Storage-"+bucket_name,
        TemplateURL="https://file-storage-security.s3.amazonaws.com/latest/templates/FSS-Storage-Stack.template",
        Parameters=[ExternalID, S3BucketToScan, scanner_queue_url, Trigger_with_event, scanner_aws_account, S3_Encryption],
        Capabilities=['CAPABILITY_IAM'],
    )
    cft_waiter = cft_client.get_waiter('stack_create_complete')
    cft_waiter.wait(StackName="C1-FSS-Storage-"+bucket_name)
    res = cft_client.describe_stacks(StackName="C1-FSS-Storage-"+bucket_name)
    storage_stack = res['Stacks'][0]['Outputs'][2]['OutputValue']
    logger.info("FSS StorageRole Arn: " + storage_stack)
    print(storage_stack)
    #add to c1
    payload = {
        "type": "storage",
        "scannerStack": stack_id,
        "provider": "aws",
        "details": {
            "managementRole": storage_stack
        }
    }
    encoded_msg = json.dumps(payload).encode('utf-8')
    resp = http.request('POST', post_url, headers = {'Content-Type': 'application/json', 'api-secret-key': fss_key, 'Api-Version': 'v1'}, body=encoded_msg)
    transform = json.loads(resp.data.decode('utf-8'))
    print(transform)
    logger.info("Storage Stack has deployed")