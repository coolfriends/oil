import boto3

class CloudFrontBarrel():
    def __init__(self, client=None):
        self.client = client or boto3.client('cloudfront')

    def tap(self, call):
        if call == 'list_distributions':
            return self.list_distributions()
        else:
            # Should throw an error
            return []

    def list_distributions(self):
        paginator = self.client.get_paginator('list_distributions')
        response_iterator = paginator.paginate()
        items_list = []

        for page in response_iterator:
            items_list.extend(page['DistributionList'].get('Items', []))

        return items_list
