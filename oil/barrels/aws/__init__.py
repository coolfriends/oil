from oil.barrels.aws.autoscaling import AutoScalingBarrel
from oil.barrels.aws.configservice import ConfigServiceBarrel
from oil.barrels.aws.cloudfront import CloudFrontBarrel
from oil.barrels.aws.cloudtrail import CloudTrailBarrel
from oil.barrels.aws.cloudwatchlogs import CloudWatchLogsBarrel
from oil.barrels.aws.iam import IAMBarrel
from oil.barrels.aws.ec2 import EC2Barrel
from oil.barrels.aws.lambda_barrel import LambdaBarrel
from oil.barrels.aws.rds import RDSBarrel
from oil.barrels.aws.redshift_barrel import RedShiftBarrel
from oil.barrels.aws.ses_barrel import SESBarrel
from oil.barrels.aws.sts import STSBarrel

core_barrels = [
    AutoScalingBarrel,
    ConfigServiceBarrel,
    CloudFrontBarrel,
    CloudTrailBarrel,
    CloudWatchLogsBarrel,
    IAMBarrel,
    EC2Barrel,
    LambdaBarrel,
    RDSBarrel,
    RedShiftBarrel,
    SESBarrel,
    STSBarrel,
]
