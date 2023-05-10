#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_workshop.pipeline_stack import WorkshopPipelineStack
from cdk_workshop.cdk_workshop_stack import CdkWorkshopStack


app = cdk.App()
CdkWorkshopStack(app, "cdk-workshop")
WorkshopPipelineStack(app, 'WorkshopPipelineStack')
app.synth()
