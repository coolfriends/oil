from oil.barrels.barrel import Barrel


class IAMBarrel(Barrel):
    _default_regions = set([
        'aws-global'
    ])
    provider = 'aws'
    service = 'iam'
    tap_calls = set([
        'get_credential_report',
    ])

    def get_credential_report(self):
        users_by_region = {}
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
            users_by_region[region] = report
        return users_by_region

    def _generate_credential_report(self, client):
        response = client.generate_credential_report()
        while response['State'].lower() != 'complete':
            response = client.generate_credential_report()
