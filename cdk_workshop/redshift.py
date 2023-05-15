from constructs import Construct
from aws_cdk import (
    Stack,
    CfnParameter,
    aws_redshift as _redshift,
    aws_secretsmanager as _sm,
    aws_iam as _iam,
    aws_ec2 as _ec2,
    RemovalPolicy,
)

class GlobalArgs():
    """
    Define Global arguments. 
    """
    VERSION='1.0.0'

class RedshiftStack(Stack):

    def __init__(self, scope:Construct, id: str, config: dict, **kwargs) -> None:
    #def __init__(self, scope:Construct, id: str, vpc: _ec2.Vpc, secret_name: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ## Secret
        ## Create Cluster credentials - when we want to use new cred in SM. 
        # cluster_secret = _sm.Secret(self, 'RedshiftCredential',
        #         description='For Redshift Cluster Secret',
        #         secret_name='RedshiftCrecential',
        #         removal_policy=RemovalPolicy.DESTROY
        # )
        ## Get Cluster credentials - when we already imported cred in SM. 
        secret = _sm.Secret.from_secret_name_v2(self, 'RedshiftSecret', config["secret-name"])

        ## Get VPC info
        vpc = _ec2.Vpc.from_lookup(self, "VPC", vpc_id=config["vpc-id"])

        ## Redshift IAM role
        cluster_iam_role = _iam.Role(self, 'RedshiftRole',
            assumed_by=_iam.ServicePrincipal('redshift.amazonaws.com'),
            managed_policies= [_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3ReadOnlyAccess')]
        )

        ## Redshift SG
        cluster_sg = _ec2.SecurityGroup(self, 'RedshiftSG',
            vpc=vpc, 
            allow_all_outbound=True, 
            security_group_name='RedshiftSG')
        
        cluster_sg.add_ingress_rule(
            peer=_ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=_ec2.Port.tcp(5439),
            description='Allow Redshift access from inside the VPC'
        )

        ## Redshift Subnet Group
        cluster_subnet_group = _redshift.CfnClusterSubnetGroup(
            self, 'RedshiftSubnetGroup',
            subnet_ids=config["subnet-ids"],
            description='Redshift Subnet Group',
        ) 

        ## Redshift Cluster
        redshift_cluster = _redshift.CfnCluster(self, 'RedshiftCluster',
            cluster_type='multi-node',
            number_of_nodes=2,
            cluster_identifier='redshift-cluster',
            master_username=secret.secret_value_from_json('username').unsafe_unwrap(),
            master_user_password=secret.secret_value_from_json('password').unsafe_unwrap(),
            node_type='dc2.large',
            cluster_subnet_group_name=cluster_subnet_group.ref,
            vpc_security_group_ids=[cluster_sg.security_group_id],
            db_name='redshift-admindb'
            )
        
        self.cluster=redshift_cluster
