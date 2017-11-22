import boto3


class Barrel():
    supported_regions = set()
    provider = None
    service = None
    tap_calls = set()

    def __init__(self, oil, **kwargs):
        self.oil = oil
        self.config = kwargs.get('config', {})
        self.session = boto3.session.Session(
            aws_access_key_id=kwargs.get('aws_access_key_id'),
            aws_secret_access_key=kwargs.get('aws_secret_access_key'),
            aws_session_token=kwargs.get('session_token'),
        )
        self.regions = kwargs.get('regions', self.supported_regions)
        self.clients = kwargs.get('clients')
        if self.clients is None:
            self.clients = self._make_clients()

    def _make_clients(self):
        clients = {}
        for region in self.regions:
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
