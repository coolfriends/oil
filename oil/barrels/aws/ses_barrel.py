from oil.barrels.barrel import Barrel


class SESBarrel(Barrel):
    supported_regions = set([
        'us-east-1',
        'us-west-2',
        'eu-west-1',
    ])
    provider = 'aws'
    service = 'ses'
    tap_calls = set([
        'list_identities',
        'get_identity_dkim_attributes',
    ])

    def __init__(self, oil, **kwargs):
        super().__init__(oil, **kwargs)
        self.cache = {}

    def list_identities(self):
        if self.cache.get('list_identities'):
            return self.cache['list_identities']

        identities_by_region = {}
        for region, client in self.clients.items():
            paginator = self.clients[region].get_paginator(
                'list_identities',
            )
            response_iterator = paginator.paginate()
            identities = []

            for page in response_iterator:
                identities.extend(page['Identities'])

            identities_by_region[region] = identities

        self.cache['list_identities'] = identities_by_region
        return identities_by_region

    def get_identity_dkim_attributes(self):
        """
        Note: There is a hard limit of 100 for identities sent into the
        getIdentityDkimAttributes API call. Additional logic will be needed
        if we need to expand functionality to accounts that exceed 100
        identities in a region.
        """
        identities_by_region = self.list_identities()

        attributes_by_region = {}
        for region, client in self.clients.items():
            identities = identities_by_region[region]

            response = client.get_identity_dkim_attributes(
                Identities=identities
            )

            attributes_by_region[region] = response['DkimAttributes']

        self.cache['get_identity_dkim_attributes'] = attributes_by_region

        return attributes_by_region
