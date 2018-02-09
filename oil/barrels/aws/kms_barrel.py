from oil.barrels.barrel import Barrel


class KMSBarrel(Barrel):
    supported_regions = set([
        'us-east-2',
        'us-east-1',
        'us-west-1',
        'us-west-2',
        'ap-northeast-1',
        'ap-northeast-2',
        'ap-south-1',
        'ap-southeast-1',
        'ap-southeast-2',
        'ca-central-1',
        'eu-central-1',
        'eu-west-1',
        'eu-west-2',
        'eu-west-3',
        'sa-east-1',
    ])
    provider = 'aws'
    service = 'kms'
    tap_calls = set([
        'describe_key',
        'get_key_rotation_status',
    ])
    paginators = {
        'list_keys': ['Keys'],
    }

    def __init__(self, oil, **kwargs):
        super().__init__(oil, **kwargs)
        self.cache = {}

    def describe_key(self):
        items_by_region = {}
        for region, client in self.clients.items():
            items_by_region[region] = {}
            for key in self.tap('list_keys')[region]:
                key_id = key['KeyId']
                response = client.describe_key(
                    KeyId=key_id
                )

                items_by_region[region][key_id] = response['KeyMetadata']

        self.cache['describe_key'] = items_by_region

        return items_by_region

    def get_key_rotation_status(self):
        items_by_region = {}
        for region, client in self.clients.items():
            items_by_region[region] = {}
            for key in self.tap('list_keys')[region]:
                key_id = key['KeyId']
                response = client.get_key_rotation_status(
                    KeyId=key_id
                )

                items_by_region[region][key_id] = response

        self.cache['get_key_rotation_status'] = items_by_region

        return items_by_region
