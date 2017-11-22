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
    ])

    def __init__(self, oil, **kwargs):
        super().__init__(oil, **kwargs)

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
        security_groups_by_region = {}
        for region, client in self.clients.items():
            paginator = client.get_paginator('describe_security_groups')

            response_iterator = paginator.paginate()
            groups = []

            for page in response_iterator:
                groups.extend(page.get('SecurityGroups', []))

            security_groups_by_region[region] = groups

        return security_groups_by_region
