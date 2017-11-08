class TLSProtocolPlugin():

    name = 'tls_protocol'
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
            certificate = distribution.get('ViewerCertificate', {})
            protocol_version = certificate.get('MinimumProtocolVersion', '')
            if not protocol_version:
                severity = 3
                message = 'No protocol version found'
            elif protocol_version == 'SSLv3':
                severity = 2
                message = '{} is insecure'.format(protocol_version)
            elif protocol_version in ['TLSv1', 'TLSv1_2016', 'TLSv1.2_2018']:
                severity = 1
                message = '{} is not considered best practice'.format(protocol_version)
            elif protocol_version == 'TLSv1.1_2016':
                severity = 0
                message = '{} is secure and considered best practice'.format(protocol_version)
            else:
                severity = 3
                message = '{} is an unexpected protocol'.format(protocol_version)

            results.append({
                'resource': resource_arn,
                'region': 'aws-global',
                'severity': severity,
                'message': message
            })

        return results
