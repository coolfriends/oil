from oil.plugins import Plugin


class TLSProtocolPlugin(Plugin):

    name = 'tls_protocol'
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

            self.results.append({
                'resource': resource_arn,
                'region': 'aws-global',
                'severity': severity,
                'message': message
            })

        return self.results
