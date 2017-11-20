from oil.barrels.barrel import Barrel


class CloudFrontBarrel(Barrel):
    _default_regions = set([
        'aws-global'
    ])
    provider = 'aws'
    service = 'cloudfront'
    tap_calls = set([
        'list_distributions',
    ])

    def __init__(self, oil, **kwargs):
        super().__init__(oil, **kwargs)

    def list_distributions(self):
        distributions_by_region = {}
        for region, client in self.clients.items():
            paginator = self.clients['aws-global'].get_paginator(
                'list_distributions',
            )
            response_iterator = paginator.paginate()
            distributions = []

            for page in response_iterator:
                distributions.extend(page['DistributionList'].get('Items', []))

            distributions_by_region[region] = distributions

        return distributions_by_region
