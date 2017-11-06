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
        'eu-west-2'
        'sa-east-1'
    ])

    def __init__(self, client=None):
        self.client = client or boto3.client('ec2')

    def describe_instances(self):
        paginator = self.client.get_paginator('describe_instances')
        response_iterator = paginator.paginate()
        instances = []

        for page in response_iterator:
            for reservation in page['Reservations']:
                instances.extend(reservation.get('Instances', []))

        return instances
