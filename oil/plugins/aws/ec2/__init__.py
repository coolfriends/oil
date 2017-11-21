from oil.plugins.aws.ec2.instance_name_tag import InstanceNameTagPlugin
from oil.plugins.aws.ec2.public_ip import PublicIpPlugin

core_plugins = [
    InstanceNameTagPlugin,
    PublicIpPlugin,
]
