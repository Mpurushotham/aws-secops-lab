from aws_cdk import (
    App, Stack,
    aws_lambda as _lambda
)
from constructs import Construct

class LambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        _lambda.Function(
            self, "DemoLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",  # 👈 index.py + handler()
            code=_lambda.Code.from_asset("lambda")
        )

app = App()
LambdaStack(app, "LambdaStack")
app.synth()