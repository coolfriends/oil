import boto3


class Barrel():
    supported_regions = set()
    provider = None
    service = None
    tap_calls = set()
    paginators = {}

    def __init__(self, oil, **kwargs):
        self.oil = oil
        self.config = kwargs.get('config', {})
        self.session = boto3.session.Session(
            aws_access_key_id=kwargs.get('aws_access_key_id'),
            aws_secret_access_key=kwargs.get('aws_secret_access_key'),
            aws_session_token=kwargs.get('session_token'),
        )
        self.cache = {}
        self.regions = kwargs.get('regions', self.supported_regions)
        self.clients = kwargs.get('clients')
        if self.clients is None:
            self.clients = self._make_clients()

    def paginate(self, call):
        if self.cache.get(call):
            return self.cache[call]

        items_by_region = {}
        for region, client in self.clients.items():
            paginator = self.clients[region].get_paginator(call)
            response_iterator = paginator.paginate()
            items = []

            for page in response_iterator:
                item = None
                for obj_key in self.paginators[call]:
                    if item is None:
                        item = page.get(obj_key, {})
                    else:
                        print(item)
                        item = item[obj_key]
                items.extend(item)

            items_by_region[region] = items

        return items_by_region

    def _make_clients(self):
        clients = {}
        for region in self.regions:
            clients[region] = self.session.client(
                self.service,
                region_name=region,
            )
        return clients

    def tap(self, call):
        if hasattr(self, call):
            return getattr(self, call)()
        if call in self.paginators.keys():
            return self.paginate(call)

        raise RuntimeError('The api call {} is not implemented'.format(
            call,
        ))
