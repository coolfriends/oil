from oil.barrels.barrel import Barrel


class SESBarrel(Barrel):
    supported_regions = set([
        'us-east-1',
        'us-west-2',
        'eu-west-1',
    ])
    provider = 'aws'
    service = 'autoscaling'
    tap_calls = set([
        'describe_auto_scaling_groups',
    ])

    def __init__(self, oil, **kwargs):
        super().__init__(oil, **kwargs)
        self.cache = {}

    def list_identities(self):
        identities_by_region = {}
        for region, client in self.clients.items():
            paginator = self.clients[region].get_paginator(
                'list_identities',
            )
            response_iterator = paginator.paginate()
            identities = []

            for page in response_iterator:
                identities.extend(page['Identities'])

            identities_by_region[region] = identities

        self.cache['list_identities'] = identities_by_region
        return identities_by_region
