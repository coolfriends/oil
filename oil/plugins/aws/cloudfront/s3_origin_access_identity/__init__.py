class S3OriginAccessIdentityPlugin():
    name = 's3_origin_access_identity'
    provider = 'aws'
    service = 'cloudfront'

    required_api_calls = {
        'aws': {
            'cloudfront': [
                'list_distributions'
            ]
        }
    }

    def __init__(self, config={}):
        """
        TODO: Set up sensible default config
        TODO: Set up configurable variables
        """
        self.config = config

    def run(self, api_data):
        results = []
        distributions = api_data['aws']['cloudfront']['aws-global']['list_distributions']

        if not distributions:
            results.append({
                'resource': 'None',
                'region': 'aws-global',
                'severity': 0,
                'message': 'No distributions found'
            })

        for distribution in distributions:
            resource_arn = distribution['ARN']
            origins = distribution.get('Origins', {})
            origin_items = origins.get('Items', [])

            if not origin_items:
                results.append({
                    'resource': resource_arn,
                    'region': 'aws-global',
                    'severity': 0,
                    'message': 'No origins found for this distribution'
                })

            for origin in origin_items:
                origin_config = origin.get('S3OriginConfig')
                if origin_config is None:
                    results.append({
                        'resource': resource_arn,
                        'region': 'aws-global',
                        'severity': 0,
                        'message': (
                            'Distribution does not have S3 origin configured'
                        )
                    })
                else:
                    access_identity = origin_config.get('OriginAccessIdentity')
                    if access_identity:
                        severity = 0
                        message = (
                            'Distribution is using secure origin {}'.format(
                                access_identity
                            )
                        )
                    else:
                        severity = 2
                        message = (
                            'Distribution is using S3 origin without an origin '
                            'access identity'
                        )
                    results.append({
                        'resource': resource_arn,
                        'region': 'aws-global',
                        'severity': severity,
                        'message': message
                    })

        return results
