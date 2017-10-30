class CloudFrontRefinery(Refinery):
    """ A higher level abstraction over boto3 CloudFront operations
    """

    required_clients = ['cloudfront']

    def __init__(self, clients):
        self.clients = clients

    def list_distributions(self):
        client = self.clients['cloudfront']

        paginator = client.get_paginator('list_distributions')
        pagination_iterator = paginator.paginate()

        distributions = []
        for page in pagination_iterator:
            distributions.extend(page['DistributionList']['Items'])

        return distributions

