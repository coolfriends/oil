from oil.barrels.barrel import Barrel


class CloudWatchLogsBarrel(Barrel):
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
        'cn-north-1'
        'cn-northwest-1',
        'eu-central-1',
        'eu-west-1',
        'eu-west-2',
        'eu-west-3',
        'sa-east-1',
    ])
    provider = 'aws'
    service = 'cloudwatchlogs'
    tap_calls = set([
        'describe_metric_filters',
    ])

    def __init__(self, oil, **kwargs):
        super().__init__(oil, **kwargs)

    def _make_clients(self):
        """ Overload because cloudwatchlogs is not the correct boto3 service.

        Reference:
        http://boto3.readthedocs.io/en/latest/reference/services/logs.html#CloudWatchLogs.Client
        """
        clients = {}
        for region in self.regions:
            clients[region] = self.session.client(
                'logs',
                region_name=region,
            )
        return clients

    def describe_metric_filters(self):
        filters_by_region = {}
        for region, client in self.clients.items():
            paginator = self.clients[region].get_paginator(
                'describe_metric_filters',
            )
            response_iterator = paginator.paginate()
            filters = []

            for page in response_iterator:
                filters.extend(page['metricFilters'])

            filters_by_region[region] = filters

        return filters_by_region
