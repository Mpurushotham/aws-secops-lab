from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
)
from constructs import Construct

class QredSecOpsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        _lambda.Function(
            self, "QredLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=_lambda.Code.from_asset("../lambda"),
        )