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
        """

        Example
          barrel = ELBBarrel()
          results = barrel.describe_load_balancer_attributes()

        Returns
          {
            'us-east-1': {
              'ALoadBalancer': {
                ... # Attributes like CrossZoneLoadBalancing, AccessLog
              }
            }
          }

        Depends on describe_load_balancers
        """
        items = {}
        for region, client in self.clients.items():
            items[region] = {}

            for load_balancer in self.tap('describe_load_balancers')[region]:
                response = client.describe_load_balancer_attributes(
                    LoadBalancerName=load_balancer['LoadBalancerName']
                )
                items[region][load_balancer['LoadBalancerName']] = response['LoadBalancerAttributes']

        return items

    def describe_load_balancer_policies(self):
        """
        Example
          barrel = ELBBarrel()
          results = barrel.describe_load_balancer_attributes()

        Returns
          {
            'us-east-1': {
              'ALoadBalancer': {
                ... # Attributes like CrossZoneLoadBalancing, AccessLog
              }
            }
          }

        Depends on describe_load_balancers
        """
        policies_by_region = {}
        for region, client in self.clients.items():
            policies_by_region[region] = {}

            for load_balancer in self.tap('describe_load_balancers')[region]:
                response = client.describe_load_balancer_policies(
                    LoadBalancerName=load_balancer['LoadBalancerName']
                )
                policies_by_region[region][load_balancer['LoadBalancerName']] = response['PolicyDescriptions']
        return policies_by_region
