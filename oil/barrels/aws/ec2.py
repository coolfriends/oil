import boto3

class EC2Barrel():
    """
    TODO: Extend barrel to work for multiple regions by leveraging multiple clients
    """
    _default_regions = set([
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

    def __init__(self, clients=None):
        self.clients = clients or self._default_clients()

    def _default_clients(self):
        clients = {}
        for region in self._default_regions:
            clients[region] = boto3.client('ec2', region_name=region)
        return clients

    def tap(self, call):
        if call == 'describe_instances':
            return self.describe_instances()
        if call == 'describe_security_groups':
            return self.describe_security_groups()
        else:
            raise RuntimeError('The api call {} is not implemented'.format(call))

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
