#!/usr/bin/env python3
import aws_cdk as cdk
from cdk_stack import SecureServerlessStack

app = cdk.App()
SecureServerlessStack(app, "SecureServerlessStack")
app.synth()
