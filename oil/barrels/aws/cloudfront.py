import boto3

class CloudFrontBarrel():
    def list_distributions(self):
        cloudfront = boto3.client('cloudfront')
        paginator = cloudfront.get_paginator('list_distributions')
        response_iterator = paginator.paginate()
        items_list = []

        for page in response_iterator:
            items_list.extend(page['DistributionList']['Items'])

        return items_list
