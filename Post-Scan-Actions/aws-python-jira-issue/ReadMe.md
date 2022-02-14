# Cloud One File Storage Security Post Scan Action - Jira Issue Create

After a malicious scan event occurs, this example Lambda function creates an issue in Jira.

## Prerequisites

1. **Obtain the following Jira values**
    - Create a [Jira API token](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)
    - Obtain your [Jira Project Key](https://confluence.atlassian.com/jirakb/how-to-get-project-id-from-the-jira-user-interface-827341414.html)
    - Copy down your **Jira URL** 
    - Identify member by **Assignee ID** to assign incoming Issues
    - Note down your **Email address** used to sign into Jira.
2. **Find the 'ScanResultTopicARN' SNS topic ARN**
    - In the AWS console, go to **Services > CloudFormation** > your all-in-one stack > **Outputs**  or **Services > CloudFormation** > your storage stack > **Outputs**.
    - Scroll down to locate the  **ScanResultTopicARN** Key.
    - Copy the **ScanResultTopic** ARN to a temporary location. Example: `arn:aws:sns:us-east-1:123445678901:FileStorageSecurity-All-In-One-Stack-StorageStack-1IDPU1PZ2W5RN-ScanResultTopic-N8DD2JH1GRKF`

## Installation

### From AWS Lambda Console

1. Visit [the app's page on the AWS Lambda Console](https://console.aws.amazon.com/lambda/home?region=us-east-1#/create/app?applicationId=arn:aws:serverlessrepo:us-east-1:024368254241:applications/CloudOne-FSS-Plugin-Jira-Issue).
2. Fill in the parameters.
3. Check the `I acknowledge that this app creates custom IAM roles.` checkbox.
4. Click `Deploy`.


## Test the Application

To test that the application was deployed properly, you'll need to generate a malware detection using the [eicar test file](https://secure.eicar.org/eicar.com "A file used for testing anti-malware scanners."), and then check the Jira project Issues to make sure the event was sent successfully.

1. **Download the Eicar test file**
   - Temporarily disable your virus scanner or create an exception, otherwise it will catch the `eicar` file and delete it.
   - Browser: Go to the [eicar file](https://secure.eicar.org/eicar.com) page and download `eicar_com.zip` or any of the other versions of this file.
   - CLI: `curl -O https://secure.eicar.org/eicar_com.zip`
2. **Upload the eicar file to the ScanningBucket**

    - Using the AWS console

        1. Go to **CloudFormation > Stacks** > your all-in-one stack > your nested storage stack.
        2. In the main pane, click the **Outputs** tab and then copy the **ScanningBucket** string. Search the string in Amazon S3 console to find your ScanningBucket.
        3. Click **Upload** and upload `eicar_com.zip`. File Storage Security scans the file and detects malware.
        4. Check your Jira Project for the new Issue creation.

    - Using the AWS CLI

        - Enter the folowing AWS CLI command to upload the Eicar test file to the scanning bucket:
            `aws s3 cp eicar_com.zip s3://<YOUR_SCANNING_BUCKET>`
        - where:
            - `<YOUR_SCANNING_BUCKET>` is replaced with the ScanningBucket name.

