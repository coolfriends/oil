from oil.barrels.barrel import Barrel


class SQSBarrel(Barrel):
    supported_regions = set([
        'us-east-2',
        'us-east-1',
        'us-west-1',
        'us-west-2',
        'ap-south-1',
        'ap-northeast-2',
        'ap-southeast-1',
        'ap-southeast-2',
        'ap-northeast-1',
        'ca-central-1',
        'eu-west-1',
        'eu-west-2',
        'eu-west-3',
        'sa-east-1'
    ])
    provider = 'aws'
    service = 'sqs'
    tap_calls = set([
        'get_queue_attributes',
        'list_queues'
    ])

    def __init__(self, oil, **kwargs):
        super().__init__(oil, **kwargs)

    def list_queues(self):
        if self.cache.get('list_queues'):
            return self.cache['list_queues']

        items = {}
        for region, client in self.clients.items():
            items[region] = []
            response = client.list_queues()
            items[region].extend(response['QueueUrls'])

        return items

    def get_queue_attributes(self):
        if self.cache.get('get_queue_attributes'):
            return self.cache['get_queue_attributes']

        items = {}
        for region, client in self.clients.items():
            items[region] = {}
            for queue in self.tap('list_queues')[region]:
                response = client.get_queue_attributes(
                    QueueUrl=queue
                )
                items[region][queue] = response['Attributes']

        return items
