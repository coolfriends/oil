class HTTPSPlugin():
    name = 'https'
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
            viewer_policy = distribution.get('ViewerProtocolPolicy')

            if not viewer_policy:
                severity = 3
                message = 'No viewer policy found for this distribution'
            elif viewer_policy == 'allow-all':
                severity = 2
                message = 'Distribution should only allow HTTPS traffic'
            elif viewer_policy == 'redirect-to-https':
                severity = 0
                message = (
                    'Distribution is properly configured to redirect HTTP '
                    'traffic to HTTPS'
                )
            elif viewer_policy == 'https-only':
                severity = 0
                message = (
                    'Distribution is properly configured to only allow HTTPS '
                    'traffic'
                )
            else:
                severity = 3
                message = (
                    'Unsupported ViewerProtocolPolicy of {}'
                ).format(viewer_policy)

            results.append({
                'resource': resource_arn,
                'region': 'aws-global',
                'severity': severity,
                'message': message
            })

        return results
