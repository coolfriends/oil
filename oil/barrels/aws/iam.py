import boto3


class IAMBarrel():
    _default_regions = set([
        'aws-global'
    ])

    def __init__(self, clients=None):
        self.clients = clients or self._default_clients()

    def _default_clients(self):
        clients = {}
        for region in self._default_regions:
            clients[region] = boto3.client('cloudfront', region_name=region)
        return clients

    def tap(self, call):
        if call == 'get_credential_report':
            return self.get_credential_report()
        else:
            raise RuntimeError('The api call {} is not implemented'.format(call))

    def get_credential_report(self):
        report_by_region = {}
        for region, client in self.clients.items():
            self._generate_credential_report(client)
            response = client.get_credential_report()
            content = response['Content'].decode('utf-8')

            report = []

            rows = content.split('\n')
            header_keys = rows[0].split(',')
            for row in rows[1:]:
                user = {}
                for index, column in enumerate(row.split(',')):
                    user[header_keys[index]] = column
                report.append(user)
            report_by_region[region] = user
        return report_by_region



    def _generate_credential_report(self, client):
        response = client.generate_credential_report()
        while response['State'].lower() != 'complete':
            response = client.generate_credential_report()

