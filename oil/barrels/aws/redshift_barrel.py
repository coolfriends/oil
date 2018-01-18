from oil.barrels.barrel import Barrel


class RedShiftBarrel(Barrel):
    supported_regions = set([
        'us-east-2',
        'us-east-1',
        'us-west-1',
        'us-west-2',
        'ap-northeast-1',
        'ap-northeast-2',
        'ap-south-1',
        'ap-southheast-1',
        'ap-southheast-2',
        'ca-central-1',
        'eu-central-1',
        'eu-west-1',
        'eu-west-2',
        'eu-west-3',
        'sa-east-1',
    ])
    provider = 'aws'
    service = 'lambda'
    tap_calls = set([
        'describe_clusters',
    ])

    def __init__(self, oil, **kwargs):
        super().__init__(oil, **kwargs)

    def describe_clusters(self):
        clusters_by_region = {}
        for region, client in self.clients.items():
            paginator = client.get_paginator(
                'describe_clusters'
            )
            response_iterator = paginator.paginate()

            functions = []
            for page in response_iterator:
                functions.extend(page.get('Clusters', []))

            clusters_by_region[region] = functions

        return clusters_by_region
