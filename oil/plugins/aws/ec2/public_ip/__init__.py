from oil.plugins import Plugin


class PublicIpPlugin(Plugin):

    name = 'public_ip'
    service = 'ec2'
    provider = 'aws'

    requirements = {
        'instances': ['aws', 'ec2', 'describe_instances']
    }

    def run(self, api_data):
        """
        TODO: Update to new documentation format
        TODO: Allow user to configure this plugin to use custom tag for Name
              (incase the user has a system set up where they use InstanceName,
               or even InStaNcE NAMe)
        """
        requirements = self.collect_requirements(api_data)
        instances_by_region = requirements['instances']
        for region, instances in instances_by_region.items():
            if not instances:
                self.results.append({
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
                    self.results.append({
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
                            self.results.append({
                                'resource': instance_id,
                                'severity': 1,
                                'region': region,
                                'message': message

                            })

                if not found:
                    self.results.append({
                        'resource': instance_id,
                        'severity': 0,
                        'region': region,
                        'message': 'Instance has no public ips'
                    })

        return self.results
