from oil.barrels.barrel import Barrel


class Route53DomainsBarrel(Barrel):
    supported_regions = set([
        'us-east-1',
    ])
    provider = 'aws'
    service = 'route53domains'
    tap_calls = set([
        'list_domains',
    ])

    def __init__(self, oil, **kwargs):
        super().__init__(oil, **kwargs)

    def list_domains(self):
        domains_by_region = {}
        for region, client in self.clients.items():
            paginator = self.clients[region].get_paginator(
                'list_domains',
            )
            response_iterator = paginator.paginate()
            domains = []

            for page in response_iterator:
                domains.extend(page['Domains'])

            domains_by_region[region] = domains

        return domains_by_region
