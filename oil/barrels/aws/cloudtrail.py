from oil.barrels.barrel import Barrel


class CloudTrailBarrel(Barrel):
    supported_regions = set([
        'us-east-2',
        'us-east-1',
        'us-west-2',
        'us-west-1',
        'ca-central-1',
        'ap-northeast-1',
        'ap-northeast-2',
        'ap-south-1',
        'ap-southheast-1',
        'ap-southheast-2',
        'cn-northwest-1',
        'eu-central-1',
        'eu-west-1',
        'eu-west-2',
        'eu-west-3',
        'sa-east-1',
    ])
    provider = 'aws'
    service = 'cloudtrail'
    tap_calls = set([
        'describe_trails',
    ])

    def __init__(self, oil, **kwargs):
        super().__init__(oil, **kwargs)

    def describe_trails(self):
        trails_by_region = {}
        for region, client in self.clients.items():
            response = self.clients[region].describe_trails()

            trails = response.get('trailList', [])
            trails_by_region[region] = trails

        return trails_by_region
