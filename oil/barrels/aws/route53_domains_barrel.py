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
    paginators = {
        'list_domains': ['Domains']
    }

    def __init__(self, oil, **kwargs):
        super().__init__(oil, **kwargs)
