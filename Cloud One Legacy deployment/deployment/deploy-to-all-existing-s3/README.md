Under Work!!- Not ready

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
      - StackName: `Enter name for stack`
   * Obtain your Cloud One API Key
      - Generate API Key: [Cloud One Workload Security API Key](https://cloudone.trendmicro.com/docs/file-storage-security/api-create-stack/#Prerequisite)

<hr>

**1. Clone Repo**
 - Clone this repository
 - After cloning repo:
 ```
   cd .\File-Storage-Security-C1\deployment\deploy-to-all-existing-s3\
```

**2. Edit Exlusions File**
   * Update/Edit the file called `exclude.txt` with names of S3 buckets to exclude from FSS deployment.
   - 1 per line, Example: [exclude.txt](https://github.com/JustinDPerkins/FSS-Storage-Automation-Lambda/deployment/deploy-to-all-existing-s3/exclude.txt)

**3. Run Script**
   - Open terminal/cmd:
   ```
      .\deploy_to_existing.py --account <aws account id> --scanner <Scanner Stack Name> --sqs <SQS URL> --apikey <WS-API-Key>
   ```  
