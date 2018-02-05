from oil.barrels.barrel import Barrel


class ELBBarrel(Barrel):
    supported_regions = set([
        'us-east-2',
        'us-east-1',
        'us-west-1',
        'us-west-2',
        'ca-central-1',
        'ap-south-1',
        'ap-northeast-2',
        'ap-northeast-1',
        'ap-southeast-2',
        'ap-southeast-1',
        'cn-northwest-1',
        'eu-central-1',
        'eu-west-1',
        'eu-west-2',
        'eu-west-3',
        'sa-east-1'
    ])
    provider = 'aws'
    service = 'elb'
    tap_calls = set([
        'describe_load_balancer_attributes',
        'describe_load_balancer_policies',
    ])
    paginators = {
        'describe_load_balancers': ['LoadBalancers'],
    }

    def __init__(self, oil, **kwargs):
        super().__init__(oil, **kwargs)

    def describe_load_balancer_attributes(self):
        pass

    def describe_load_balancer_policies(self):
        pass
