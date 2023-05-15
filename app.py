#!/usr/bin/env python3

import aws_cdk as cdk
import json

#from cdk_workshop.pipeline_stack import WorkshopPipelineStack
#from cdk_workshop.cdk_workshop_stack import CdkWorkshopStack
from cdk_workshop.redshift import RedshiftStack


app = cdk.App()
#CdkWorkshopStack(app, "cdk-workshop")
#WorkshopPipelineStack(app, 'WorkshopPipelineStack')

#cdk.aws_ec2.Vpc.from_lookup(self, "VPC", vpc_id=vpcid)
#vpc = app.node.try_get_context("dev").vpc-id
#dev_vpc = app.node.try_get_context("dev")["vpc-id"]
#dev_secret_name = app.node.try_get_context("dev")["secret-name"]

with open('cdk.json') as cdkfile:
    cdk_json = json.loads(cdkfile.read())

region = app.node.try_get_context("globals")["region"]

environment = app.node.try_get_context("environments")
if environment == "prod":
    config = cdk_json["context"]["environments"]["prod"]
else:
    config = cdk_json["context"]["environments"]["dev"]
print(config)

_env = cdk.Environment(account=config["account"], region=region)

#RedshiftStack(app, 'RedshiftStack', vpc=dev_vpc, secret_name=dev_secret_name)
RedshiftStack(app, 'RedshiftStack', config, env=_env)


app.synth()
