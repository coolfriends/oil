from oil.barrels.aws.autoscaling import AutoScalingBarrel
from oil.barrels.aws.cloudfront import CloudFrontBarrel
from oil.barrels.aws.cloudtrail import CloudTrailBarrel
from oil.barrels.aws.cloudwatchlogs import CloudWatchLogsBarrel
from oil.barrels.aws.iam import IAMBarrel
from oil.barrels.aws.ec2 import EC2Barrel
from oil.barrels.aws.rds import RDSBarrel

core_barrels = [
    AutoScalingBarrel,
    CloudFrontBarrel,
    CloudTrailBarrel,
    IAMBarrel,
    EC2Barrel,
    RDSBarrel,
]
