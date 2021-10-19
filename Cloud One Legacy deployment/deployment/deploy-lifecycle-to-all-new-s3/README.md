# Automation using Lambda to Deploy/Remove FSS- Storage Stack 


![architecture](architecture.png)

# Automate complete S3 FSS lifecycle Stack Deployment/Removal
`Note: FSS Bucket Lifecycle Automation Stack. Deploy FSS Storage to each new S3 bucket. When S3 Bucket is deleted FSS stack is removed if monitored`
<details>
<summary>Deploy via CloudFormation</summary>

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
      - Select: **[automate_add_remove_fss_storage_stack.yaml]https://github.com/JustinDPerkins/File-Storage-Security-C1/blob/main/deployment/deploy-lifecycle-to-all-new-s3/cloudformation/automate_add_remove_fss_storage_stack.yaml)**
      - Click **Next**
      - StackName: `Enter name for stack`
      - C1WSAPI: [Cloud One Workload Security API Key](https://cloudone.trendmicro.com/docs/file-storage-security/api-create-stack/#Prerequisite)
      - SQSURL: `http://scanner-stack-sqs-queue-url.com`
      - StackName: `Enter name of Scanner Stack`
      - Click **Create Stack**
</details>    
<hr>

# Automate Storage Stack Deployment 
`Note: Automated process to deploy an FSS storage stack on each new S3 bucket using Lambda. The storage stack will be linked to the scanner stack previously defined.`
<details>
<summary>Deploy via CloudFormation</summary>

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
      - Select: **[storage_stack.yaml](https://github.com/JustinDPerkins/File-Storage-Security-C1/blob/main/deployment/deploy-lifecycle-to-all-new-s3/cloudformation/storage_stack.yaml)**
      - Click **Next**
      - StackName: `Enter name for stack`
      - C1WSAPI: [Cloud One Workload Security API Key](https://cloudone.trendmicro.com/docs/file-storage-security/api-create-stack/#Prerequisite)
      - SQSURL: `http://scanner-stack-sqs-queue-url.com`
      - StackName: `Enter name of Scanner Stack`
      - Click **Create Stack**
</details>      
<hr>

# Automate Storage Stack Removal
`Note: Automated process to remove an FSS storage stack on each deleted S3 bucket event using Lambda. If the S3 bucket has an associated FSS Storage Stack it will be removed.`
<details>
<summary>Deploy via CloudFormation</summary>
  
* Go to AWS Console > Services > CloudFormation
    - Click **Create New Stack**
      - Prerequisites: `template is ready`
      - Specify Template: `upload from file`
      - Select: **[implode_storage_stack.yaml](https://github.com/JustinDPerkins/File-Storage-Security-C1/blob/main/deployment/deploy-lifecycle-to-all-new-s3/cloudformation/implode_storage_stack.yaml)**
      - Click **Next**
      - StackName: `Enter name for stack`
      - C1WSAPI: [Cloud One Workload Security API Key](https://cloudone.trendmicro.com/docs/file-storage-security/api-create-stack/#Prerequisite)
      - Click **Create Stack**
  
</details>
<hr>

# A Note on Tags

The Lambda will choose whether or not to deploy a storage stack depending on a bucket's tags. **See below for details**:

| Tag            | Value  | Behavior                       |
| -------------- | ------ | ------------------------------ |
| [no tag]       | [none] | Storage Stack deployed         |
| `FSSMonitored` | `yes`  | Storage Stack deployed         |
| `FSSMonitored` | `no`   | Storage Stack **NOT** deployed |

The script will add the proper tags automatically to untagged buckets, but you can *exclude* buckets by adding a `FSSMonitored` == `no` tag. 
