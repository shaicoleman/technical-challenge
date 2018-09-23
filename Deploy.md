# Serverless deployment to AWS Lambda with Up

* Install and configure AWS CLI and environment variables
```
export AWS_DEFAULT_REGION=eu-west-1
export AWS_PROFILE=aylien
aws configure --profile $AWS_PROFILE
```
* Install the [Up serverless framework](https://up.docs.apex.sh/)
* Run `cd app`
* Run `up deploy` to deploy after setting up the environment variables above
* Run `up url` to view the deployed website URL

Note: Prometheus monitoring is disabled on Lambda
