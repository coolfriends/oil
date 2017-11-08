class PublicIpPlugin():

    name = 'public_ip'
    service = 'ec2'
    provider = 'aws'

    required_api_calls = {
        'aws': {
            'ec2': [
                'describe_instances'
            ]
        }
    }

    def __init__(self, config={}):
        """
        TODO: Add configurable variables
        """
        self.config = config

    def run(self, api_data):
        """
        TODO: Update to new documentation format
        TODO: Allow user to configure this plugin to use custom tag for Name
              (incase the user has a system set up where they use InstanceName,
               or even InStaNcE NAMe)
        """
        results = []
        for region, api_calls in api_data['aws']['ec2'].items():
            instances = api_calls['describe_instances']
            if not instances:
                results.append({
                    'resource': 'None',
                    'region': region,
                    'severity': 0,
                    'message': 'No instances found'
                })
            for instance in instances:
                instance_id = instance['InstanceId']

                found = False
                public_ip = instance.get('PublicIpAddress', '')
                if public_ip:
                    found = True
                    message = 'Instance has public ip: {}'.format(public_ip)
                    results.append({
                        'resource': instance_id,
                        'severity': 1,
                        'region': region,
                        'message': message
                    })

                network_interfaces = instance.get('NetworkInterfaces', [])
                for network_interface in network_interfaces:
                    association = network_interface.get('Association', {})
                    association_public_ip = association.get('PublicIp', '')

                    # Make sure not to double record public ip
                    if association_public_ip:
                        if association_public_ip != public_ip:
                            found = True
                            message = (
                                'Instance has public ip: {}'.format(
                                    association_public_ip
                                )
                            )
                            results.append({
                                'resource': instance_id,
                                'severity': 1,
                                'region': region,
                                'message': message

                            })


                if not found:
                    results.append({
                        'resource': instance_id,
                        'severity': 0,
                        'region': region,
                        'message': 'Instance has no public ips'
                    })

        return results
