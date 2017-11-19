import boto3


class Barrel():
    _default_regions = set()
    provider = None
    service = None
    tap_calls = set()

    def __init__(self, oil, config={}, clients=None):
        self.oil = oil
        self.config = config
        self.session = boto3.session.Session()
        self.clients = clients or self._default_clients()

    def _default_clients(self):
        clients = {}
        for region in self._default_regions:
            clients[region] = self.session.client(
                self.service,
                region_name=region,
            )
        return clients

    def tap(self, call):
        if call in self.tap_calls:
            return getattr(self, call)()

        raise RuntimeError('The api call {} is not implemented'.format(
            call,
        ))
