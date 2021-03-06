from oil.barrels.barrel import Barrel


class RDSBarrel(Barrel):
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
        'sa-east-1',
    ])
    provider = 'aws'
    service = 'rds'
    tap_calls = set([
        'describe_db_instances',
        'describe_db_security_groups',
    ])

    def __init__(self, oil, **kwargs):
        super().__init__(oil, **kwargs)

    def describe_db_instances(self):
        db_instances_by_region = {}
        for region, client in self.clients.items():
            paginator = client.get_paginator(
                'describe_db_instances'
            )
            response_iterator = paginator.paginate()
            db_instances = []

            for page in response_iterator:
                db_instances.extend(page.get('DBInstances', []))

            db_instances_by_region[region] = db_instances

        return db_instances_by_region

    def describe_db_security_groups(self):
        db_security_groups_by_region = {}
        for region, client in self.clients.items():
            paginator = client.get_paginator(
                'describe_db_security_groups'
            )
            response_iterator = paginator.paginate()
            db_instances = []

            for page in response_iterator:
                db_instances.extend(page.get('DBSecurityGroups', []))

            db_security_groups_by_region[region] = db_instances

        return db_security_groups_by_region
