# Deploy Schedule Scan Plugin to all exisitng S3
This script will deploy The Cloud One - FSS scheduled full scan plugin stack to all storage stacks linked to a defined Scanner. After a plugin deployment the Scanner Stacks SQS Access Policy will be updated to include the needed AWS Principals. 

**Requirements**

* Obtain your **Cloud One API Key**.
   - Generate API Key: [Cloud One API Key](https://cloudone.trendmicro.com/docs/account-and-user-management/c1-api-key/)

* Obtain your **Cloud One Region**.
   - Sign in to your **Cloud One console > Administration > Account Settings**.
   -  Copy the value of the **Region**.

* Obtain the following values from the Already deployed FSS Scanner Stack:
   - Go to **AWS Console > Services > CloudFormation**
   - Click on the **Name of your Scanner Stack**
      - Select the **OutPuts Tab**
      - Copy the name of your **Scanner Stack** 
      - Copy the value of thev**ScannerQueueURL**
   
   * **Obtain/Create the AWS Profile name to be used for the AWS Account the Scanner Stack was deployed.**
      - Creating an AWS Profile: [Create Profile](https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/keys-profiles-credentials.html) 
      ```
      [SCANNER-AWS-ACCOUNT-PROFILE]
      aws_access_key_id = YOUR_ACCESS_KEY_ID_FOR_ACCOUNT_WITH_SCANNER
      aws_secret_access_key = YOUR_SECRET_ACCESS_KEY_FOR_ACCOUNT_WITH_SCANNER
      ```
   
   

---


**Run Script**
   - Open terminal/cmd:

   - **Configure AWS CLI to interact with AWS Account where FSS Storage Stacks Are deployed.**
   ```
   aws configure
   ```
   
   - Run the Commands below in the same directory as the script:

   [Windows]
   ```
      .\full_scan_deploy.py --c1region <cloud one region; example: us-1> --scanner <Scanner Stack Name> --apikey <CloudOne-API-Key> --profile <AWS profile name. AWS account with Scanner Stack>
   ```  
   
   [Mac/Linux]
   ```
     python3 full_scan_deploy.py --c1region <cloud one region; example: us-1> --scanner <Scanner Stack Name> --apikey <CloudOne-API-Key> --profile <AWS profile name. AWS account with Scanner Stack>
   ```

---

# Additional Notes


### Supported FSS regions

Please note this script supports only S3 buckets deployed in [AWS Regions File Storage Security Supports](https://cloudone.trendmicro.com/docs/file-storage-security/supported-aws/#AWSRegion). Buckets deployed in unsupported FSS AWS regions need to be excluded from deployemnts.
