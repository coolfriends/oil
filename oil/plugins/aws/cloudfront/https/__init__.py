from oil.plugins import Plugin


class HTTPSPlugin(Plugin):
    name = 'https'
    provider = 'aws'
    service = 'cloudfront'

    requirements = {
        'distributions': ['aws', 'cloudfront', 'list_distributions']
    }


    def run(self, api_data):
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
            cache_behavior = distribution.get('DefaultCacheBehavior', {})
            viewer_policy = cache_behavior.get('ViewerProtocolPolicy', '')

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

            self.results.append({
                'resource': resource_arn,
                'region': 'aws-global',
                'severity': severity,
                'message': message
            })

        return self.results
