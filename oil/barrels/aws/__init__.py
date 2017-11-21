from oil.barrels.aws.cloudfront import CloudFrontBarrel
from oil.barrels.aws.iam import IAMBarrel
from oil.barrels.aws.ec2 import EC2Barrel
from oil.barrels.aws.rds import RDSBarrel

core_barrels = [
    CloudFrontBarrel,
    IAMBarrel,
    EC2Barrel,
    RDSBarrel,
]
