from oil.plugins.aws.cloudfront import core_plugins as cloudfront_core_plugins
from oil.plugins.aws.iam import core_plugins as iam_core_plugins
from oil.plugins.aws.ec2 import core_plugins as ec2_core_plugins
from oil.plugins.aws.rds import core_plugins as rds_core_plugins

core_plugins = []
core_plugins.extend(cloudfront_core_plugins)
core_plugins.extend(iam_core_plugins)
core_plugins.extend(ec2_core_plugins)
core_plugins.extend(rds_core_plugins)
