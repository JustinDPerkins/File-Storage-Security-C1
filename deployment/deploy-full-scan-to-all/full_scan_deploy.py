#from http.client import responses
import json
import time
import re
import boto3
import argparse
import urllib3
from botocore.config import Config
from botocore.exceptions import ClientError

http = urllib3.PoolManager()

# Argument variables needed
parser = argparse.ArgumentParser(description='Deploy to All Buckets')
parser.add_argument("--c1region", required=True, type=str, help="Cloud One Account Region")
parser.add_argument("--scanner", required=True, type=str, help="FSS Scanner Stack Name")
parser.add_argument("--apikey", required=True, type=str, help="Cloud One API Key")
parser.add_argument("--profile", required=True, type=str, help="Define AWS profile to be used to access AWS account scanner is in")
args = parser.parse_args()

scanner_stack_name = args.scanner
cloud_one_region = args.c1region
ws_api = args.apikey 
aws_profile = args.profile 
stacks_api_url = "https://filestorage." + cloud_one_region + ".cloudone.trendmicro.com/api/"

# list scanner stacks in fss for obtaining id, sqs arn, sqs url, scanner region
def list_scanner_stacks():
    # fss get all scanner stacks call
    id_call = http.request('GET', stacks_api_url + "stacks", fields={"limit": "100", "type": "scanner"},
                           headers={'Authorization': 'ApiKey ' + ws_api, 'Api-Version': 'v1'})
    try:
        id_resp = json.loads(id_call.data.decode('utf-8'))['stacks']
    except json.decoder.JSONDecodeError:
        time.sleep(1)
        id_resp = json.loads(id_call.data.decode('utf-8'))['stacks']
    # read all scanner stacks call, get the stack-id, sqsURL, and last format an SQS ARN
    for data in id_resp:
        if 'name' in data and data['name'] is not None:
            if scanner_stack_name == data['name']:
                # gather scanner stack id
                stack_id = data['stackID']
                # gather sqs url
                scannerQueueURL = data['details']['scannerQueueURL']
                # gather Scanner region
                scannerRegion = data['details']['region']
                #transform_url(scannerQueueURL)
                pattern = re.compile(r"https://sqs\.(.*)\.amazonaws\.com/(.*)/(.*)")
                match = pattern.search(scannerQueueURL)
                if match:
                    region = match.group(1)
                    account = match.group(2)
                    queue_name = match.group(3)
                    # gather sqs arn
                    sqs = (f"arn:aws:sqs:{region}:{account}:{queue_name}")
                    
                else:
                    return None
                gather_storage_stacks(stack_id, scannerQueueURL, sqs, scannerRegion)

# function for gathering Scanner stacks associated Storage Stacks. 
def gather_storage_stacks(stack_id, scannerQueueURL, sqs, scannerRegion):
    # gather all linked storage stacks to obtain bucket name, the region it lives, and the name of the storage stack cft.
    storage_listing = http.request('GET', stacks_api_url + "stacks?scannerStack="+stack_id,
                           headers={'Authorization': 'ApiKey ' + ws_api, 'Api-Version': 'v1'})
    try:
        storage_resp = json.loads(storage_listing.data.decode('utf-8'))['stacks']
    except json.decoder.JSONDecodeError:
        time.sleep(1)
        storage_resp = json.loads(storage_listing.data.decode('utf-8'))['stacks']
    if storage_resp == []:
        print("No Storage Stack(s) have been associated to: "+scanner_stack_name)
        exit
    for storage in storage_resp:
        #bucket name
        bucket = storage['storage']
        #bucket region
        bucket_region = storage['details']['region']
        # cft storage stack name in AWS.
        storage_stack_name = storage['name']
        cft_storage_stacks_arns(bucket, bucket_region, storage_stack_name, scannerQueueURL, sqs, scannerRegion)

# funtion to gather sns arn from AWS cft storage stacks value outputs. 
def cft_storage_stacks_arns(bucket, bucket_region, storage_stack_name, scannerQueueURL, sqs, scannerRegion):
    cfn = boto3.client('cloudformation')
    region = bucket_region
    # describe stack outputs
    try:
        response = cfn.describe_stacks(StackName=storage_stack_name)
        stack = response['Stacks'][0]
        outputs = {output['OutputKey']: output['OutputValue'] for output in stack['Outputs']}
        # gather sns topic ARN
        sns = outputs['ScanResultTopicARN']
        deploy_full_scan(bucket, region, sqs, scannerQueueURL, sns, scannerRegion)
    except ClientError:
        print(storage_stack_name+" does not exist in this particular AWS Account. Skipping")
# Function to deploy full scan plugin in AWS region bucket exists in.
def deploy_full_scan(bucket,region, sqs, scannerQueueURL, sns, scannerRegion):
    my_region_config = Config(
        region_name=region,
        signature_version='v4',
        retries={
            'max_attempts': 10,
            'mode': 'standard'
        }
    )
    # define paramters to be used to deploy cft stack
    BucketName = {"ParameterKey": "BucketName", "ParameterValue": bucket}
    ScannerQueueArn = {"ParameterKey": "ScannerQueueArn", "ParameterValue": sqs}
    ScannerQueueUrl = {"ParameterKey": "ScannerQueueUrl", "ParameterValue": scannerQueueURL}
    ScanResultTopicArn = {"ParameterKey": "ScanResultTopicArn", "ParameterValue": sns}
    Schedule = {"ParameterKey": "Schedule", "ParameterValue": ""}
    cfn = boto3.client("cloudformation", config=my_region_config)
    cfbucketname = bucket.replace(".", "-")
    try:
        # create the aws cft stack
        cfn.create_stack(
            StackName="full-scan-" + cfbucketname,
            TemplateURL="https://aws-workshop-c1as-cft-templates.s3.amazonaws.com/sar-full-scan.yaml",
            Parameters=[
                BucketName,
                ScannerQueueArn,
                ScannerQueueUrl,
                ScanResultTopicArn,
                Schedule,
            ],
            Capabilities=["CAPABILITY_IAM", "CAPABILITY_AUTO_EXPAND"],
        )
        # wait for cft stack to complete
        print("Deploying Schedule Scan Plugin to : " + bucket )
        cft_waiter = cfn.get_waiter("stack_create_complete")
        cft_waiter.wait(StackName="full-scan-" + cfbucketname)
        # get cft output values after completed
        res = cfn.describe_stacks(StackName="full-scan-" + cfbucketname)
        lambda_iam_arn = (res['Stacks'][0]['Outputs'][0]['OutputValue'])
        update_sqs_policy(lambda_iam_arn, scannerQueueURL, scannerRegion)
    except ClientError:
        print("Schedule Scan plugin already exists in AWS for "+cfbucketname+". Skipping")

# Add the plugin full_scan functions iam role arn to the existing SQS acccess policy
def update_sqs_policy(lambda_iam_arn, scannerQueueURL, scannerRegion):
    #switch to a new profile for Scanner Account
    session = boto3.Session(profile_name=aws_profile, region_name=scannerRegion)
    sqs = session.client('sqs')
    # Get the current SQS queue policy
    queue_policy_response = sqs.get_queue_attributes(
        QueueUrl=scannerQueueURL,
        AttributeNames=['Policy']
    )
    # isolate policy AWS principals
    queue_policy_json = queue_policy_response['Attributes']['Policy']
    queue_policy = json.loads(queue_policy_json)
    iam_policy = queue_policy['Statement'][0]['Principal']['AWS']
    # add the full scans to the existing allowed sqs principals list
    iam_policy.append(lambda_iam_arn)
    queue_policy['Statement'][0]['Principal']['AWS'].append(iam_policy)
    remove_value = (len(queue_policy['Statement'][0]['Principal']['AWS']) - 1)
    iam_policy.pop(remove_value)
    
    print('Updating Scanner SQS Access policy to allow: '+lambda_iam_arn)
    # Set the updated SQS queue policy
    latest_policy = sqs.set_queue_attributes(
        QueueUrl=scannerQueueURL,
        Attributes={
            'Policy': json.dumps((queue_policy))
        }
    )
 # call first function   
list_scanner_stacks()

