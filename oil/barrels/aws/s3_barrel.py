from oil.barrels.barrel import Barrel


class S3Barrel(Barrel):
    supported_regions = set([
        'us-east-2',
        'us-east-1',
        'us-west-1',
        'us-west-2',
        'ca-central-1',
        'ap-south-1',
        'ap-northeast-2',
        'ap-southeast-1',
        'ap-southeast-2',
        'ap-northeast-1',
        'eu-west-1',
        'eu-west-2',
        'eu-west-3',
        'sa-east-1'
    ])
    provider = 'aws'
    service = 's3'
    tap_calls = set([
        'list_buckets',
        'get_bucket_acl',
        'get_bucket_versioning'
    ])

    def __init__(self, oil, **kwargs):
        super().__init__(oil, **kwargs)

    def list_buckets(self):
        if self.cache.get('list_buckets'):
            return self.cache['list_buckets']

        items = {}
        for region, client in self.clients.items():
            items[region] = []
            response = client.list_buckets()
            items[region].extend(response['Buckets'])

        return items

    def get_bucket_acl(self):
        if self.cache.get('get_bucket_acl'):
            return self.cache['get_bucket_acl']

        items = {}
        for region, client in self.clients.items():
            items[region] = {}
            for bucket in self.tap('list_buckets')[region]:
                response = client.get_bucket_acl(
                    Bucket=bucket['Name']
                )
                items[region][bucket['Name']] = response['Grants']

        return items

    def get_bucket_versioning(self):
        if self.cache.get('get_bucket_versioning'):
            return self.cache['get_bucket_versioning']

        items = {}
        for region, client in self.clients.items():
            items[region] = {}
            for bucket in self.tap('list_buckets')[region]:
                response = client.get_bucket_versioning(
                    Bucket=bucket['Name']
                )
                items[region][bucket['Name']] = response

        return items
