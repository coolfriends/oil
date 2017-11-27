from oil.barrels.barrel import Barrel


class EC2Barrel(Barrel):
    """
    TODO: Extend barrel to work for multiple regions by leveraging
    multiple clients
    """
    supported_regions = set([
        'us-east-2',
        'us-east-1',
        'us-west-1',
        'us-west-2',
        'ap-south-1',
        'ap-northeast-1',
        'ap-northeast-2',
        'ap-southeast-1',
        'ap-southeast-2',
        'ca-central-1',
        'eu-central-1',
        'eu-west-1',
        'eu-west-2',
        'sa-east-1'
    ])
    provider = 'aws'
    service = 'ec2'
    tap_calls = set([
        'describe_instances',
        'describe_security_groups',
        'high_threat_security_groups',
    ])
    default_high_threat_ports = [
        80,    # HTTP
        443,   # HTTPS
        3389,  # RDS
    ]

    def __init__(self, oil, **kwargs):
        super().__init__(oil, **kwargs)
        self.cache = {}
        self.high_threat_ports = kwargs.get('high_threat_ports',
                                            self.default_high_threat_ports)

    def describe_instances(self):
        instances_by_region = {}
        for region, client in self.clients.items():
            paginator = client.get_paginator('describe_instances')

            response_iterator = paginator.paginate()
            instances = []

            for page in response_iterator:
                for reservation in page['Reservations']:
                    instances.extend(reservation.get('Instances', []))

            instances_by_region[region] = instances

        return instances_by_region

    def describe_security_groups(self):
        if self.cache.get('describe_security_groups'):
            return self.cache['describe_security_groups']

        security_groups_by_region = {}
        for region, client in self.clients.items():
            paginator = client.get_paginator('describe_security_groups')

            response_iterator = paginator.paginate()
            groups = []

            for page in response_iterator:
                groups.extend(page.get('SecurityGroups', []))

            security_groups_by_region[region] = groups

        self.cache['describe_security_groups'] = security_groups_by_region
        return security_groups_by_region

    def high_threat_security_groups(self):
        high_threat_groups_by_region = {}
        for region, security_groups in self.describe_security_groups().items():
            high_threat_groups = []
            for security_group in security_groups:
                found_ports = self.find_high_threat_ports(security_group)
                if found_ports:
                    high_threat_groups.append({
                        'id': security_group['GroupId'],
                        'ports': found_ports,
                    })

            high_threat_groups_by_region[region] = high_threat_groups

        return high_threat_groups_by_region

    def find_high_threat_ports(self, security_group):
        ports = []
        for rule in security_group['IpPermissions']:
            if rule.get('FromPort') in self.high_threat_ports:
                ports.append(rule['FromPort'])

        return ports
