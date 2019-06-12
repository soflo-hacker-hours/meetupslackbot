# Environment variables

```
export AWS_PROFILE=default
export AWS_PACKAGE_BUCKET=uniqueBucketName
export AWS_STACK_NAME=MySFHHMeetupSlackBot
export SAM_BUILD_FILE=./build/package.yaml
export SLACKWEBHOOKURL=https://hooks.slack.com/services/this/that/more
```

# Preparation

## Installation

* https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
* https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html

## Create build bucket

```
aws s3 mb s3://${AWS_PACKAGE_BUCKET}
```

# Deploy environment

## Package for AWS

```
sam package --s3-bucket ${AWS_PACKAGE_BUCKET} --template-file ./template.yaml --output-template-file ${SAM_BUILD_FILE}
```

## Deploy to AWS

```
sam deploy --template-file ${SAM_BUILD_FILE} --stack-name ${AWS_STACK_NAME} --capabilities CAPABILITY_IAM  --parameter-overrides SlackWebHook=${SLACKWEBHOOKURL}
```

## Configure Slack

* Add a bot
* Create New Command (hard coded to be /meetup)
* Request URL should be the URL found in AWS Stack Outputs with /api appended
