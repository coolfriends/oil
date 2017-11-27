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
        'high_threat_message': {
            'name': 'High Threat Message',
            'description': (
                'Message to display if an instance has a '
                'high threat port open'
            ),
            'value_description': '{port} {group_id}',
            'default': 'Port {port} open on group {group_id}',
        },
        'high_threat_severity': {
            'name': 'High Threat Severity',
            'description': (
                'Severity level for a instance with a '
                'high threat port open'
            ),
            'value_description': '0 1 2',
            'default': 2,
        },
        'no_high_threat_display': {
            'name': 'No Instances Display',
            'description': (
                'Choose whether to display a message when an instance does '
                'not have a high threat port open'
            ),
            'value_description': 'True or False',
            'default': True,
        },
        'no_high_threat_message': {
            'name': 'No Instances Message',
            'description': 'Change the message for instances in a region',
            'value_description': 'string',
            'default': 'Instance has no high threat ports open',
        },
        'no_instances_display': {
            'name': 'No Instances Display',
            'description': (
                'Choose whether to display no instances message in results',
            ),
            'value_description': 'True or False',
            'default': True,
        },
        'no_instances_message': {
            'name': 'No Instances Message',
            'description': 'Change the message for instances in a region',
            'value_description': 'string',
            'default': 'No instances found',
        },
    }

    def run(self, api_data):
        # Reset the results list for this plugin
        self.results = []

        requirements = self.collect_requirements(api_data)
        instances_by_region = requirements['instances']
        high_threat_groups_by_region = requirements['groups']

        for region, instances in instances_by_region.items():
            if not instances and self.config['no_instances_display']:
                self.results.append({
                    'resource': 'None',
                    'region': region,
                    'severity': 0,
                    'message': self.config['no_instances_message'],
                })

            for instance in instances:
                found = False
                resource = instance['InstanceId']

                for group in instance.get('SecurityGroups', []):
                    high_threat_groups = high_threat_groups_by_region[region]
                    for high_threat_group in high_threat_groups:
                        if group['GroupId'] == high_threat_group['id']:
                            found = True
                            for high_threat_port in high_threat_group['ports']:
                                self.results.append({
                                    'resource': resource,
                                    'region': region,
                                    'severity': self.config.get(
                                        'high_threat_severity'
                                    ),
                                    'message': self.config.get(
                                        'high_threat_message'
                                    ).format(
                                        port=high_threat_port,
                                        group_id=group['GroupId'],
                                    )
                                })

                if not found and self.config['no_high_threat_display']:
                    self.results.append({
                        'resource': resource,
                        'region': region,
                        'severity': 0,
                        'message': self.config['no_high_threat_message'],
                    })

        return self.results
