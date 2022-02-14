# Cloud One File Storage Security Post Scan Action - Slack

After a malicious scan event occurs, this example Lambda function sends a notification in Slack.

## Prerequisites

1. **Configure Slack Webhook App**
    - Create a Slack Channel to receive the notification
    - Go to App Directory > Search `Incoming WebHooks`.
    - Click on `Incoming WebHooks`, then click "Add to Slack"
    - Choose the Channel to receive the notification
    - Copy Webhook URL
    - Enter the Description of your WebHook.
    - Enter the Name of the Slack WebHook, by default it will use `incoming-webhook`; if you prefer, you can customize the name.
    - If you want any custom icon to add that in Customize Icon section.
    - Click "Save Setting"
    
    [Additional information](https://slack.com/help/articles/115005265063-Incoming-webhooks-for-Slack)

2. **Find the 'ScanResultTopicARN' SNS topic ARN**
    - In the AWS console, go to **Services > CloudFormation** > your all-in-one stack > **Outputs**  or **Services > CloudFormation** > your storage stack > **Outputs**.
    - Scroll down to locate the  **ScanResultTopicARN** Key.
    - Copy the **ScanResultTopic** ARN to a temporary location. Example: `arn:aws:sns:us-east-1:123445678901:FileStorageSecurity-All-In-One-Stack-StorageStack-1IDPU1PZ2W5RN-ScanResultTopic-N8DD2JH1GRKF`

## Installation

### From AWS Lambda Console

1. Visit [the app's page on the AWS Lambda Console](https://console.aws.amazon.com/lambda/home?#/create/app?applicationId=arn:aws:serverlessrepo:us-east-1:415485722356:applications/cloudone-filestorage-plugin-action-promote-or-quarantine).
2. Fill in the parameters.
3. Check the `I acknowledge that this app creates custom IAM roles.` checkbox.
4. Click `Deploy`.


## Test the Application

To test that the application was deployed properly, you'll need to generate a malware detection using the [eicar test file](https://secure.eicar.org/eicar.com "A file used for testing anti-malware scanners."), and then check the Slack notification to make sure the event was sent successfully.

1. **Download the Eicar test file**
   - Temporarily disable your virus scanner or create an exception, otherwise it will catch the `eicar` file and delete it.
   - Browser: Go to the [eicar file](https://secure.eicar.org/eicar.com) page and download `eicar_com.zip` or any of the other versions of this file.
   - CLI: `curl -O https://secure.eicar.org/eicar_com.zip`
2. **Upload the eicar file to the ScanningBucket**

    - Using the AWS console

        1. Go to **CloudFormation > Stacks** > your all-in-one stack > your nested storage stack.
        2. In the main pane, click the **Outputs** tab and then copy the **ScanningBucket** string. Search the string in Amazon S3 console to find your ScanningBucket.
        3. Click **Upload** and upload `eicar_com.zip`. File Storage Security scans the file and detects malware.
        4. Check your Slack channel for the event.

    - Using the AWS CLI

        - Enter the folowing AWS CLI command to upload the Eicar test file to the scanning bucket:
            `aws s3 cp eicar_com.zip s3://<YOUR_SCANNING_BUCKET>`
        - where:
            - `<YOUR_SCANNING_BUCKET>` is replaced with the ScanningBucket name.