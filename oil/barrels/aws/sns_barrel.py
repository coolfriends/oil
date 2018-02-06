from oil.barrels.barrel import Barrel


class SNSBarrel(Barrel):
    supported_regions = set([
        'us-east-2',
        'us-east-1',
        'us-west-1',
        'us-west-2',
        'ca-central-1',
        'ap-south-1',
        'ap-northeast-2',
        'ap-southeast-2',
        'ap-northeast-1',
        'eu-central-1',
        'eu-west-1',
        'eu-west-3',
    ])
    provider = 'aws'
    service = 'sns'
    tap_calls = set([
        'get_topic_attributes',
    ])
    paginators = {
        'list_topics': ['Topics']
    }

    def __init__(self, oil, **kwargs):
        super().__init__(oil, **kwargs)

    def get_topic_attributes(self):
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

            for topic in self.tap('list_topics')[region]:
                response = client.get_topic_attributes(
                    TopicArn=topic['TopicArn']
                )
                items[region][topic['TopicArn']] = response['Attributes']

        return items
