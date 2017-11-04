class TLSProtocolPlugin():
    def run(self, data):
        results = []

        if not data:
            results.append({
                'resource': 'None',
                'region': 'aws-global',
                'severity': 0,
                'message': 'No distributions found'
            })

        for item in data:
            resource_arn = item['ARN']
            protocol_version = item['ViewerCertificate']['MinimumProtocolVersion']
            if protocol_version == 'SSLv3':
                severity = 2
                message = '{} is insecure'.format(protocol_version)
            elif protocol_version in ['TLSv1', 'TLSv1_2016', 'TLSv1.2_2018']:
                severity = 1
                message = '{} is not considered best practice'.format(protocol_version)
            elif protocol_version == 'TLSv1.1_2016':
                severity = 0
                message = '{} is secure and considered best practice'.format(protocol_version)
            else:
                severity = '3'
                message = '{} is an unexpected protocol'.format(protocol_version)

            results.append({
                'resource': resource_arn,
                'region': 'aws-global',
                'severity': severity,
                'message': message
            })

        return results
