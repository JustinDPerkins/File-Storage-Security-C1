# Cloud One - File Storage Security Plugins.

This repo contains plugins to leverage with Trend Micro Cloud One - File Storage Security


## Deploy File Storage Stack to ALL existing buckets

To deploy File Storage Security storage stack to S3 buckets that currently exist in your AWS account.
   - Go to [Deploy to Existing](https://github.com/JustinDPerkins/FSS-Storage-Automation-Lambda/tree/main/deployment/deploy-to-all-existing-s3)

## Automate File Storage Stack S3 lifecycle Deployment/Removal to all new buckets

To automatically deploy File Storage Security to newly created S3 buckets.
   - Go to [Deploy to future resources](https://github.com/JustinDPerkins/FSS-Storage-Automation-Lambda/tree/main/deployment/deploy-lifecycle-to-all-new-s3)

## Before you deploy

You will need:
   - AWS Account ID
   - Cloud One API key
   - Successfully Deployed Scanner Stack
   - Scanner Stack Name
   - Scanner Stack SQS URL
