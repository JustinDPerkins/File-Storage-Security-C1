import urllib3
import json
import os
import base64
import boto3
http = urllib3.PoolManager()

# JIRA project set
user=os.environ['JIRA_EMAIL']
api= os.environ['JIRA_API']
projectKey = os.environ['JIRA_KEY']
url = os.environ['JIRA_URL']+"/rest/api/3/issue"
assignee = os.environ['JIRA_ASSIGNEE']


def lambda_handler(event, context):

    # get secret
    secrets = boto3.client('secretsmanager').get_secret_value(SecretId=api)
    sm_data = json.loads(secrets["SecretString"])
    jira_api = sm_data["jiraapikey"]
    
    for record in event['Records']:
        
        
        #ARN info to get AWS Account ID
        arn = json.dumps(record['EventSubscriptionArn'])
        account_id = arn.split(":")[4].strip()
        
        #Message details from SNS event
        message = json.loads(record['Sns']['Message'])
        findings = message['scanning_result'].get('Findings')

        if findings:
        
            malwares = []
            types = []
            for finding in message['scanning_result']['Findings']:
                malwares.append(finding.get('malware'))
                types.append(finding.get('type'))

            account=str(account_id)
            malwares=', '.join(malwares)
            types=', '.join(types)
            file_url=str(message['file_url'])
            
            # JIRA auth setup https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-post
            base_authentication = user + ":" + jira_api
            base_auth = str.encode(base_authentication)

            token =  "Basic " + base64.b64encode(base_auth).decode("utf-8") 
            
            # headers
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization" : token
            }
            
            # get bucket name isolated from file url
            split_file_url = file_url.split(".s3.amazonaws.com")
            isolate_bucket = split_file_url[0].split('/')
            
            # setup JIRA issue creation
            payload = json.dumps( {
            "fields": {
            "project": {"key": projectKey},
            "summary": 'Malicious Object Detected',
            "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                    {
                        "type": "paragraph",
                        "content": [
                        {
                            "type": "text",
                            "text": 'AWS Account: ' + account + "\n" + 'Bucket: ' + isolate_bucket[2] + "\n" + 'Malware Name: ' + malwares + "\n" + 'Malware Type: ' + types + "\n" + 'File Location: ' + file_url
                        }
                        ]
                    }
                    ]
                },
            "issuetype": {"name": 'Task'},
            "labels": ["malware-detected", "Trend-Micro", "File-Storage-Security", types],
            "assignee": {"id": assignee}
            }
            }
            )
            
            response = http.request(
                "POST", 
                url,
                body=payload,
                headers=headers
            )
            
            # Decode Json string to Python
            json_data = json.loads(response.data.decode("utf-8"))
            print(json_data)