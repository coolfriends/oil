from oil.barrels.barrel import Barrel


class ConfigServiceBarrel(Barrel):
    supported_regions = set([
        'us-east-2',
        'us-east-1',
        'us-west-2',
        'us-west-1',
        'ap-northeast-1',
        'ap-northeast-2',
        'ap-south-1',
        'ap-southheast-1',
        'ap-southheast-2',
        'ca-central-1',
        'cn-north-1',
        'cn-northwest-1',
        'eu-central-1',
        'eu-west-1',
        'eu-west-2',
        'eu-west-3',
        'sa-east-1',
    ])
    provider = 'aws'
    service = 'configservice'
    tap_calls = set([
        'describe_configuration_recorders',
        'describe_configuration_recorder_status',
    ])

    def __init__(self, oil, **kwargs):
        super().__init__(oil, **kwargs)

    def _make_clients(self):
        """ Overload because configservice is not the correct boto3 service.

        Reference:
        http://boto3.readthedocs.io/en/latest/reference/services/config.html#client
        """
        clients = {}
        for region in self.regions:
            clients[region] = self.session.client(
                'config',
                region_name=region,
            )
        return clients

    def describe_configuration_recorders(self):
        recorders_by_region = {}
        for region, client in self.clients.items():
            response = self.clients[region].describe_configuration_recorders()

            recorders = response.get('ConfigurationRecorders', [])
            recorders_by_region[region] = recorders

        return recorders_by_region

    def describe_configuration_recorder_status(self):
        recorders_status_by_region = {}
        for region, client in self.clients.items():
            response = self.clients[region].describe_configuration_recorder_status()

            recorders_status = response.get('ConfigurationRecordersStatus', [])
            recorders_status_by_region[region] = recorders_status

        return recorders_status_by_region
