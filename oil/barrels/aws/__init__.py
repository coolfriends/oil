from oil.barrels.aws.autoscaling import AutoScalingBarrel
from oil.barrels.aws.configservice import ConfigServiceBarrel
from oil.barrels.aws.cloudfront import CloudFrontBarrel
from oil.barrels.aws.cloudtrail import CloudTrailBarrel
from oil.barrels.aws.cloudwatchlogs import CloudWatchLogsBarrel
from oil.barrels.aws.iam import IAMBarrel
from oil.barrels.aws.ec2 import EC2Barrel
from oil.barrels.aws.elb_barrel import ELBBarrel
from oil.barrels.aws.kms_barrel import KMSBarrel
from oil.barrels.aws.lambda_barrel import LambdaBarrel
from oil.barrels.aws.rds import RDSBarrel
from oil.barrels.aws.redshift_barrel import RedShiftBarrel
from oil.barrels.aws.route53_domains_barrel import Route53DomainsBarrel
from oil.barrels.aws.s3_barrel import S3Barrel
from oil.barrels.aws.ses_barrel import SESBarrel
from oil.barrels.aws.sns_barrel import SNSBarrel
from oil.barrels.aws.sts import STSBarrel
from oil.barrels.aws.sqs_barrel import SQSBarrel

core_barrels = [
    AutoScalingBarrel,
    ConfigServiceBarrel,
    CloudFrontBarrel,
    CloudTrailBarrel,
    CloudWatchLogsBarrel,
    IAMBarrel,
    EC2Barrel,
    ELBBarrel,
    KMSBarrel,
    LambdaBarrel,
    RDSBarrel,
    RedShiftBarrel,
    Route53DomainsBarrel,
    SESBarrel,
    SNSBarrel,
    STSBarrel,
    SQSBarrel,
    S3Barrel,
]
