# Deploy to All Existing S3 Resource
This script will deploy File Storage Security Stack to all buckets unless defined in exclusions text file. After deployment the stack will be registered with Cloud One Console. 

**Before you deploy**

   * If not already present, [deploy a Scanner Stack](https://cloudone.trendmicro.com/docs/file-storage-security/stack-add/#AddScanner) in the Cloud One - File Storage Security account.
  * Obtain the Scanner Stack Name and SQS URL
      - Go to AWS Console > Services > CloudFormation
      - Click **Name of Scanner Stack**
         - Copy **Stack Name** 
      - Under **Outputs** tab
         - Copy **ScannerQueueURL**
   * Go to AWS Console > Services > CloudFormation
    - Click **Create New Stack**
      - Prerequisites: `template is ready`
      - Specify Template: `upload from file`
      - Select: **[automate_add_remove_fss_storage_stack.yaml](https://github.com/JustinDPerkins/FSS-Storage-Automation-Lambda/blob/main/cloudformation/automate_add_remove_fss_storage_stack.yaml)**
      - Click **Next**
      - StackName: `Enter name for stack`
      - C1WSAPI: [Cloud One Workload Security API Key](https://cloudone.trendmicro.com/docs/file-storage-security/api-create-stack/#Prerequisite)
      - SQSURL: `http://scanner-stack-sqs-queue-url.com`
      - StackName: `Enter name of Scanner Stack`
      - Click **Create Stack**

<hr>

**Required Variables** 
   - filename = `exclude.txt`
   - scanner_stack_name = `<Scanner Stack Name>`
   - ws_api = `<Cloud One - Workload Security API Key>`
   - sqs_url = `https://<your scanner sqs url here>`
   - aws_account_id = `<aws account id>`

**Create Exlusions File**
   * Create a file with names of S3 buckets to exclude from FSS deployment
   - 1 per line, Example: [exclude.txt](https://github.com/JustinDPerkins/FSS-Storage-Automation-Lambda/deployment/deploy-to-all-existing-s3/exclude.txt)
   - This file must be saved in same folder as the .py file.

**Run Script**
   - Navigate to the directory/folder
   - To run in cmd `.\deploy_to_existing.py`
