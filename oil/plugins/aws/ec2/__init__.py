from oil.plugins.aws.ec2.instance_name_tag import InstanceNameTagPlugin
from oil.plugins.aws.ec2.public_ip import PublicIpPlugin
from oil.plugins.aws.ec2.instance_high_threat_port import InstanceHighThreatPortPlugin

core_plugins = [
    InstanceNameTagPlugin,
    PublicIpPlugin,
    InstanceHighThreatPortPlugin,
]
