from oil.barrels.barrel import Barrel


class AutoScalingBarrel(Barrel):
    supported_regions = set([
        'us-east-2',
        'us-east-1',
        'us-west-2',
        'us-west-1',
        'ap-northeast-1',
        'ap-northeast-2',
        'ap-south-1',
        'ap-southheast-1',
        'ap-southheast-2',
        'ca-central-1',
        'cn-north-1',
        'cn-northwest-1',
        'eu-central-1',
        'eu-west-1',
        'eu-west-2',
        'eu-west-3',
        'sa-east-1',
    ])
    provider = 'aws'
    service = 'autoscaling'
    tap_calls = set([
        'describe_auto_scaling_groups',
    ])

    def __init__(self, oil, **kwargs):
        super().__init__(oil, **kwargs)

    def describe_auto_scaling_groups(self):
        groups_by_region = {}
        for region, client in self.clients.items():
            paginator = self.clients[region].get_paginator(
                'describe_auto_scaling_groups',
            )
            response_iterator = paginator.paginate()
            groups = []

            for page in response_iterator:
                groups.extend(page['AutoScalingGroups'])

            groups_by_region[region] = groups

        return groups_by_region
