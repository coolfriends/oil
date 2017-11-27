from oil.plugins import Plugin


class InstanceHighThreatPortPlugin(Plugin):

    name = 'instance_high_threat_port'
    provider = 'aws'
    service = 'ec2'

    requirements = {
        'instances': ['aws', 'ec2', 'describe_instances'],
        'groups': ['aws', 'ec2', 'high_threat_security_groups'],
    }

    default_config = {
        'root_user_enabled_message': {
            'name': 'Root User MFA Enabled Message',
            'description': 'Change the message for Root User MFA Enabled',
            'value_description': '{username}',
            'default': 'MFA enabled for {username}',
        },
        'root_user_not_enabled_message': {
            'name': 'Root User MFA Not Enabled Message',
            'description': 'Change the message for Root User MFA Not Enabled',
            'value_description': '{username}',
            'default': 'MFA not enabled for {username}',
        },
        'root_user_not_enabled_severity_level': {
            'name': 'Root User MFA Not Enabled Severity',
            'description': 'Severity for no MFA device enabled for root user',
            'value_description': '0 1 2',
            'default': 2
        },
        'enabled_message': {
            'name': 'MFA Enabled Message',
            'description': 'Change the message for MFA Enabled',
            'value_description': '{username}',
            'default': 'MFA enabled for {username}',
        },
        'not_enabled_message': {
            'name': 'MFA Not Enabled Message',
            'description': 'Change the message for MFA Not Enabled',
            'value_description': '{username}',
            'default': 'MFA not enabled for {username}',
        },
        'not_enabled_severity_level': {
            'name': 'MFA Not Enabled Severity Level',
            'description': 'Adjust the severity for no MFA device enabled',
            'value_description': '0 1 2',
            'default': 2,
        },
    }

    def run(self, api_data):
        # Reset the results list for this plugin
        self.results = []

        requirements = self.collect_requirements(api_data)
        instances_by_region = requirements['instances']
        groups_by_region = requirements['groups']

        for region, instances in instances_by_region.items():
            if not instances:
                self.results.append({
                    'resource': 'None',
                    'region': region,
                    'severity': 0,
                    'message': 'No instances found'
                })

            for instance in instances:
                found = False
                resource = instance['InstanceId']

                for group in instance.get('SecurityGroups', []):
                    for high_threat in groups_by_region[region]:
                        if group['GroupId'] == high_threat['id']:
                            found = True
                            for high_threat_port in high_threat['ports']:
                                self.results.append({
                                    'resource': resource,
                                    'region': region,
                                    'severity': 2,
                                    'message': (
                                        'High threat port open: {port}'.format(
                                            port=high_threat_port
                                        )
                                    )
                                })

                if not found:
                    self.results.append({
                        'resource': resource,
                        'region': region,
                        'severity': 0,
                        'message': (
                            'Instance does not have any high threat ports open'
                        )
                    })

        return self.results
