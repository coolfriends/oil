import boto3

class CloudFrontBarrel():
    _default_regions = set([
        'aws-global'
    ])
    provider = 'aws'
    service = 'cloudfront'

    def __init__(self, oil, config={}, clients=None):
        self.oil = oil
        self.clients = clients or self._default_clients()

    def _default_clients(self):
        clients = {}
        for region in self._default_regions:
            clients[region] = boto3.client('cloudfront', region_name=region)
        return clients

    def tap(self, call):
        if call == 'list_distributions':
            return self.list_distributions()
        else:
            raise RuntimeError('The api call {} is not implemented'.format(call))

    def list_distributions(self):
        distributions_by_region = {}
        for region, client in self.clients.items():
            paginator = self.clients['aws-global'].get_paginator('list_distributions')
            response_iterator = paginator.paginate()
            distributions = []

            for page in response_iterator:
                distributions.extend(page['DistributionList'].get('Items', []))

            distributions_by_region[region] = distributions

        return distributions_by_region
