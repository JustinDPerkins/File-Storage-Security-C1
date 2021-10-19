#!/usr/bin/env powershell

<#
.SYNOPSIS
Installs File Storage Security bucket lifecycle monitoring stack in all regions.

.DESCRIPTION
This script uses AWS CLI to look up existing Cloud One File Storage Security - Storage Stack and installs latest
template

.PARAMETER
No parameters

.EXAMPLE
event-bus-install.ps1

.NOTES
Requires AWS CLI to be installed and configured with your desired account access keys
http://docs.aws.amazon.com/cli/latest/userguide/installing.html
#>


Clear-Host

$workloadapi = "add your api key from ws console"
$scannerstack = "enter name of scanner stack"
$sqsurl = "enter scanner stack sqs url"

$templateUrl = "https://aws-workshop-c1as-cft-templates.s3.amazonaws.com/fss-automate.yaml"
$regions = @("us-east-1","us-east-2","us-west-1","us-west-2","ap-south-1","ap-northeast-2","ap-southeast-1","ap-southeast-2","ap-northeast-1","eu-central-1","eu-west-1","eu-west-2","eu-west-3","eu-north-1","sa-east-1","ca-central-1","me-south-1","ap-east-1","af-south-1","eu-south-1","ap-northeast-3")
$classicRegions = @("us-east-1","us-east-2","us-west-1","us-west-2","ap-south-1","ap-northeast-2","ap-southeast-1","ap-southeast-2","ap-northeast-1","eu-central-1","eu-west-1","eu-west-2","eu-west-3","eu-north-1","sa-east-1","ca-central-1","ap-northeast-3")
$stackName = "TM-S3-Storage-Stack-lifecycle"
$version = "1"

if (-Not(Get-Command "aws" -errorAction SilentlyContinue)) {
	Write-Warning "Please install AWS Command Line Interface first: http://docs.aws.amazon.com/cli/latest/userguide/installing.html"
	return;
}

$installedCount = 0
$updatedCount = 0
$failedCount = 0

$versionTag = "Key=Version,Value=$version"
$updateDateTag = "Key=LastUpdatedTime,Value='" + $( Get-Date ([datetime]::UtcNow) -UFormat %c ) + "'"
$accountIdParam = "ParameterKey=C1WSAPI,ParameterValue=$workloadapi"
$eventBusSourcesParam = "ParameterKey=SQSURL,ParameterValue=$sqsurl"
$eventBusSourcesParam2 = "ParameterKey=StackName,ParameterValue=$scannerstack"

function Is-Region-Enabled {
	Param($region)
	if ( $classicRegions.Contains($region)) {
		return $TRUE
	} else {
		aws sts get-caller-identity --region $region --endpoint-url https://sts.$region.amazonaws.com 2>&1> $null
		if ($lastExitCode -eq 0) {
			return $TRUE
		} else {
			return $FALSE
		}
	}
}

foreach ($region in $regions) {
	if (Is-Region-Enabled($region)) {
		"$( Get-Date ) Looking for existing $stackName stack in $region"
		aws cloudformation describe-stacks --stack-name $stackName --region $region --output json 2>&1> $null

		if ($lastExitCode -eq 0) {

			"$( Get-Date ) Updating $stackName - V$version in $region..."

			aws cloudformation update-stack `
				--stack-name $stackName `
				--region $region `
				--parameters $accountIdParam $eventBusSourcesParam $eventBusSourcesParam2 `
				--template-url $templateUrl `
				--capabilities CAPABILITY_NAMED_IAM `
				--tags $versionTag $updateDateTag > $null

			if ($lastExitCode -eq 0) {
				"$( Get-Date ) Successfully updated $stackName - V$version in $region"
				$updatedCount++
			} else {
				Write-Warning "Could not install $stackName - V$version in $region"
				$failedCount++
			}

		} else {

			"$( Get-Date ) Installing $stackName - V$version in $region..."

			aws cloudformation create-stack `
				--stack-name $stackName `
				--region $region `
				--parameters $accountIdParam $eventBusSourcesParam $eventBusSourcesParam2 `
				--template-url $templateUrl `
				--on-failure DO_NOTHING `
				--capabilities CAPABILITY_NAMED_IAM `
				--tags $versionTag $updateDateTag > $null

			if ($lastExitCode -eq 0) {
				"$( Get-Date ) Successfully installed $stackName - V$version in $region"
				$installedCount++
			} else {
				Write-Warning "Could not install $stackName - V$version in $region"
				$failedCount++
			}

		}

	} else {
		Write-Host "$( Get-Date ) Region $region is either not enabled or not supported with the current access credentials"
	}

	Write-Host ""
}

if ($failedCount -gt 0) {
	Write-Warning "Could not install or update $stackName in $failedCount region(s)."
} else {
	if ($installedCount -gt 0) {
		"Installed $stackName in $installedCount region(s) successfully."
	}
	if ($updatedCount -gt 0) {
		"Updated $stackName in $updatedCount region(s) successfully."
	}
}