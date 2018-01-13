from oil.barrels.barrel import Barrel


class STSBarrel(Barrel):
    supported_regions = set([
        'aws-global',
        'us-east-2',
        'us-east-1',
        'us-west-2',
        'us-west-1',
        'ca-central-1',
        'ap-south-1',
        'ap-northeast-2',
        'ap-northeast-1',
        'ap-southheast-1',
        'ap-southheast-2',
        'eu-central-1',
        'eu-west-1',
        'eu-west-2',
        'sa-east-1',
    ])
    provider = 'aws'
    service = 'sts'
    tap_calls = set([
        'get_caller_identity',
    ])

    def __init__(self, oil, **kwargs):
        super().__init__(oil, **kwargs)

    def get_caller_identity(self):
        identity_by_region = {}
        for region, client in self.clients.items():
            response = self.clients[region].get_caller_identity()

            identity = response
            identity_by_region[region] = identity

        return identity_by_region
