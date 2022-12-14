# Create the S3 bucket for the CodePipeline artifacts - This bucket must be globally unique
aws s3 mb s3://php1301-airflow-dev-codepipeline-artifacts
# Create IAM roles and add iniline policies so that CodePipeline can interact with EKS through kubectl
aws iam create-role --role-name AirflowCodePipelineServiceRole --assume-role-policy-document file://WeatherForecastDataPipeline/AWS/CodePipeline/dev/cpAssumeRolePolicyDocument.json
aws iam put-role-policy --role-name AirflowCodePipelineServiceRole --policy-name codepipeline-access --policy-document file://WeatherForecastDataPipeline/AWS/CodePipeline/dev/cpPolicyDocument.json
aws iam create-role --role-name AirflowCodeBuildServiceRole --assume-role-policy-document file://WeatherForecastDataPipeline/AWS/CodePipeline/dev/cbAssumeRolePolicyDocument.json
aws iam put-role-policy --role-name AirflowCodeBuildServiceRole --policy-name codebuild-access --policy-document file://WeatherForecastDataPipeline/AWS/CodePipeline/dev/cbPolicyDocument.json

# open the flux pipeline to set the bucket name you created under "ArtifactStore"
vim WeatherForecastDataPipeline/AWS/CodePipeline/dev/airflow-dev-pipeline.cfn.yml

# Create the AWS CodePipeline using CloudFormation (This doesn't deploy the image as Flux handles it)
aws cloudformation create-stack --stack-name=airflow-dev-pipeline --template-body=file://WeatherForecastDataPipeline/AWS/CodePipeline/dev/airflow-dev-pipeline.cfn.yml --parameters ParameterKey=GitHubUser,ParameterValue=php1301 ParameterKey=GitHubToken,ParameterValue= ParameterKey=GitSourceRepo,ParameterValue=wfdp-docker-eks ParameterKey=GitBranch,ParameterValue=dev
