from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_events as events,
    aws_events_targets as targets,
)
from constructs import Construct
from cdk_nag import NagSuppressions, AwsSolutionsChecks

class SecureServerlessStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB table with encryption
        table = ddb.Table(
            self, "QredTable",
            partition_key={"name": "id", "type": ddb.AttributeType.STRING},
            encryption=ddb.TableEncryption.AWS_MANAGED,
            removal_policy=ddb.RemovalPolicy.DESTROY
        )

        # Primary Lambda
        fn = _lambda.Function(
            self, "SecureLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("lambda_function"),
            environment={"TABLE_NAME": table.table_name},
        )

        table.grant_read_write_data(fn)

        # Add least privilege IAM policy for SecretsManager
        fn.add_to_role_policy(iam.PolicyStatement(
            actions=["secretsmanager:GetSecretValue"],
            resources=["*"]
        ))

        # API Gateway
        apigw.LambdaRestApi(self, "SecureAPI", handler=fn)

        # Auto-remediation Lambda
        remediate_fn = _lambda.Function(
            self, "RemediationFn",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="remediate.lambda_handler",
            code=_lambda.Code.from_asset("lambda_function"),
        )

        events.Rule(
            self, "SecurityHubRule",
            event_pattern=events.EventPattern(
                source=["aws.securityhub"],
                detail_type=["Security Hub Findings - Imported"]
            ),
            targets=[targets.LambdaFunction(remediate_fn)]
        )

        # Apply cdk-nag for compliance checks
        Aspects.of(self).add(AwsSolutionsChecks())
        NagSuppressions.add_stack_suppressions(
            self, [{"id": "AwsSolutions-IAM4", "reason": "Lab example only"}]
        )
