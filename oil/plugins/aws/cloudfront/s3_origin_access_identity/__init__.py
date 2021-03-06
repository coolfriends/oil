from oil.plugins import Plugin

class S3OriginAccessIdentityPlugin(Plugin):
    name = 's3_origin_access_identity'
    provider = 'aws'
    service = 'cloudfront'

    requirements = {
        'distributions': ['aws', 'cloudfront', 'list_distributions']
    }

    def run(self, api_data):
        # Reset the results list for this plugin
        self.results = []

        requirements = self.collect_requirements(api_data)
        distributions = requirements['distributions']['aws-global']

        if not distributions:
            self.results.append({
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
                self.results.append({
                    'resource': resource_arn,
                    'region': 'aws-global',
                    'severity': 0,
                    'message': 'No origins found for this distribution'
                })

            for origin in origin_items:
                origin_config = origin.get('S3OriginConfig')
                if origin_config is None:
                    self.results.append({
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
                    self.results.append({
                        'resource': resource_arn,
                        'region': 'aws-global',
                        'severity': severity,
                        'message': message
                    })

        return self.results
