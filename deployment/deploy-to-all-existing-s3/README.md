Under Work!!- Needs pagination handling for larger deployments

# Deploy to All Existing S3 Resource
This script will deploy File Storage Security Stack to all buckets unless defined in exclusions text file. After deployment the stack will be registered with Cloud One Console. 

**Before you deploy**

   * If not already present, [deploy a Scanner Stack](https://cloudone.trendmicro.com/docs/file-storage-security/stack-add-aws/) in the Cloud One - File Storage Security account.
  * Obtain the Scanner Stack Name and SQS URL
      - Go to AWS Console > Services > CloudFormation
      - Click **Name of Scanner Stack**
         - Copy **Stack Name** 
      - Under **Outputs** tab
         - Copy **ScannerQueueURL**
      - StackName: `Enter name for stack`
   * Obtain your Cloud One API Key
      - Generate API Key: [Cloud One API Key](https://cloudone.trendmicro.com/docs/account-and-user-management/c1-api-key/)

<hr>

**1. Clone Repo**
 - Clone this repository
 - After cloning repo:
 ```
   cd .\File-Storage-Security-C1\deployment\deploy-to-all-existing-s3\
```

**2. Edit Exclusions File**
   * Update/Edit the file called `exclude.txt` with names of S3 buckets to exclude from FSS deployment.
   - 1 per line, Example: [exclude.txt](https://github.com/JustinDPerkins/File-Storage-Security-C1/blob/main/deployment/deploy-to-all-existing-s3/exclude.txt)

**3. Run Script**
   - Open terminal/cmd:
   ```
      .\deploy.py --account <aws account id> --c1region <cloud one region; example: us-1> --scanner <Scanner Stack Name> --sqs <SQS URL> --apikey <CloudOne-API-Key>
   ```  


# A Note on Tags

The Script will choose whether or not to deploy a storage stack depending on a bucket's tags. **See below for details**:

| Tag            | Value  | Behavior                       |
| -------------- | ------ | ------------------------------ |
| [no tag]       | [none] | Storage Stack deployed         |
| `FSSMonitored` | `yes`  | Stack Already Exists(skip)     |
| `FSSMonitored` | `no`   | Storage Stack **NOT** deployed |
