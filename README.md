# Automation using Lambda to Deploy/Remove FSS- Storage Stack 

1. Automated process to deploy an FSS storage stack on each new S3 bucket using Lambda. The storage stack will be linked to the scanner stack previously defined.
2. Automated process to remove an FSS storage stack on each deleted S3 bucket event using Lambda. If the S3 bucket has an associated FSS storage Stack it will be removed.

![architecture](architecture.png)

# Automate Storage Stack Deployment 
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
      - Select: **[storage_stack.yaml](https://github.com/JustinDPerkins/FSS-Storage-Automation-Lambda/blob/main/cloudformation/storage_stack.yaml)**
      - Click **Next**
      - StackName: `Enter name for stack`
      - C1WSAPI: [Cloud One Workload Security API Key](https://cloudone.trendmicro.com/docs/file-storage-security/api-create-stack/#Prerequisite)
      - SQSURL: `http://scanner-stack-sqs-queue-url.com`
      - StackName: `Enter name of Scanner Stack`
      - Click **Create Stack**
</details>      

<details>
<summary>Deploy via AWS Console</summary>
  
   * Create IAM Role/Policy for lambda execution
   * In AWS Console > Services > IAM
      - In left panel under **Access Management** click **Policy**
      - Click **Create Policy**
         - Select **JSON**
         - paste **[fss_policy](https://github.com/JustinDPerkins/FSS-Storage-Automation-Lambda/blob/main/policy/fss_policy.json)**
         - Save
   * In AWS Console > Services > IAM
      - In left panel under **Access Management** click **Roles**
      - Create Role
         - Entity: AWS Service
         - Service: Lambda
         - select policy made previously
         - Save

   * Create Lambda Function
   * In AWS Console > Services > Lambda >  Create Function

      - Select **Author from scratch**
      - Function Name: *example-name*
      - Runtime: **Python 3.8**
      - Select Service role: **Select role created in previous steps**
      - Create Function
   * Under Code
      - Copy and Paste: **[storage_stack.yaml](https://github.com/JustinDPerkins/FSS-Storage-Automation-Lambda/blob/main/cloudformation/storage_stack.yaml)**
      - Deploy
   * Under Configuration
      - Environment Variables
      - **C1-API** : *your fss api key*
      - **SQS_Name** : *scanner sqs url*
      - **STACK_ID** : *scanner stack id*
      - See [FSS API Documentation](https://cloudone.trendmicro.com/docs/file-storage-security/api-create-stack/) for details.
      - Configuration
      - General configuration > Edit
      - increase timeout to 8m

   * Create CloudWatch Rule
   * In AWS Console > Services > CloudWatch
      - In left panel under **Events** click **Rules**
   * Create New CloudWatch Rule
      - Event Source: Event Pattern
      - Service Name: S3
      - Event Type: Bucket Level Operations
      - Specific Operation(s): CreateBucket
   * Add Target
      - Select: **Lambda Function**
      - Choose the function made in  first step
      - leave the rest to defaults
   * Configure Rule details
      - Name: *example-rule-name*
      - Description: 
      - State: **Enabled**
      - Create rule 
</details>

### A Note on Tags

The Lambda will choose whether or not to deploy a storage stack depending on a bucket's tags. **See below for details**:

| Tag            | Value  | Behavior                       |
| -------------- | ------ | ------------------------------ |
| [no tag]       | [none] | Storage Stack deployed         |
| `FSSMonitored` | `yes`  | Storage Stack deployed         |
| `FSSMonitored` | `no`   | Storage Stack **NOT** deployed |

The script will add the proper tags automatically to untagged buckets, but you can *exclude* buckets by adding a `FSSMonitored` == `no` tag. 
</details>

# Automate Storage Stack Removal
<details>
<summary>Deploy via CloudFormation</summary>
  
* Go to AWS Console > Services > CloudFormation
    - Click **Create New Stack**
      - Prerequisites: `template is ready`
      - Specify Template: `upload from file`
      - Select: **[implode_storage_stack.yaml](https://github.com/trendmicro/cloudone-filestorage-plugins/blob/master/deployment/aws-python-storage-stack-automation/implode_storage_stack.yaml)**
      - Click **Next**
      - StackName: `Enter name for stack`
      - C1WSAPI: [Cloud One Workload Security API Key](https://cloudone.trendmicro.com/docs/file-storage-security/api-create-stack/#Prerequisite)
      - Click **Create Stack**
  
</details>

<details>
<summary>Deploy via AWS Console</summary>
  
   * Create IAM Role/Policy for lambda execution
   * In AWS Console > Services > IAM
      - In left panel under **Access Management** click **Policy**
      - Click **Create Policy**
         - Select **JSON**
         - paste **[implode_policy](https://github.com/JustinDPerkins/FSS-Storage-Automation-Lambda/blob/main/policy/implode_policy.json)**
         - Save
   * In AWS Console > Services > IAM
      - In left panel under **Access Management** click **Roles**
      - Create Role
         - Entity: AWS Service
         - Service: Lambda
         - Select policy made previously
         - Save

   * Create Lambda Function
   * In AWS Console > Services > Lambda >  Create Function
      - Select **Author from scratch**
      - Function Name: *example-name*
      - Runtime: **Python 3.8**
      - Select Service role: **Select role created in previous steps**
      - Create Function
   * Under Code
      - Copy and Paste: **[implode_storage_stack.yaml](https://github.com/JustinDPerkins/FSS-Storage-Automation-Lambda/blob/main/cloudformation/implode_storage_stack.yaml)**
      - Deploy
   * Under Configuration
      - Environment Variables
      - **WS-API** : *your ws api key*
      - See [FSS API Documentation](https://cloudone.trendmicro.com/docs/file-storage-security/api-create-stack/) for details.
      - Configuration
      - General configuration > Edit
      - increase timeout to 2m

   * Create CloudWatch Rule
   * In AWS Console > Services > CloudWatch
      - In left panel under **Events** click **Rules**
   * Create New CloudWatch Rule
      - Event Source: Event Pattern
      - Service Name: S3
      - Event Type: Bucket Level Operations
      - Specific Operation(s): DeleteBucket
   * Add Target
      - Select: **Lambda Function**
      - Choose the function made in  first step
      - leave the rest to defaults
   * Configure Rule details
      - Name: *example-rule-name*
      - Description: 
      - State: **Enabled**
      - Create rule 
</details>
