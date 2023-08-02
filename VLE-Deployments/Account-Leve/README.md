# File Storage Security Account-Wide Deployment

This repo contains templates to deploy Trend Cloud One File Storage Security throughout an AWS Account.


## Deploy File Storage Security throughout AWS Account.

![Scanner-Multi-Region](images/account-wide.jpg)


### What is going on?
- The Main Template is deployed to the determined AWS Account.
- The Stack will create an IAM Role and S3 Quarantine bucket for the account and launch a stackset to create the EventBridge Rule Pattern in every AWS Region.
- Next stack deploys the File Storage Scanner Stack.
- The third Stack deploys various resources to perform the following tasks:
   - Creates a Secret in Secrets Manager for the API Key secure storage.
   - Determines any KMS Key ARN's associated with applicable existing S3 resources in that account.
   - Enables EventBridge Notifications for all existing S3 resources in that account.
   - Registers the File Storage Scanner Stack to Trend Backend for Licensing Updates.
   - Updates Scanner Stack Parameters to include quarantine and KMS Keys.
- Last the Full Schedule Scan Plugin is deployed.

---

## What is needed before you deploy

You will need:
   - AWS Account
   - Valid Cloud One Account
   - [Grant self-managed permissions for StackSets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs-self-managed.html#stacksets-prereqs-accountsetup)
   - [Full Access Cloud One API Key](https://cloudone.trendmicro.com/docs/identity-and-account-management/c1-api-key/)

---

### Deployment Steps

- **APIKey**: Value of Cloud One API Key.
- **AdminRoleARN**: ARN Value of StackSetAdministrator Role.
- **CloudOneRegion**: The region your Cloud One Tenant resides in.
- **ExternalID**: Cloud One ExternalID value.
- **RegionsToEnable**: Alternative region to where the Scanner was deployed. This will allow for events outside the main scanner region to be routed to the Scanner Stack.


[![Launch Stack](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=VLE-FSS-Stack&templateURL=https://immersionday-workshops-trendmicro.s3.amazonaws.com/fss/vle-deployment/account-wide/main.account.yaml)

--- 
