from oil.plugins import Plugin


class InstanceNameTagPlugin(Plugin):

    name = 'instance_name_tag'
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
        # Reset the results list for this plugin
        self.results = []

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
                tags = instance.get('Tags', [])
                name = None
                for tag in tags:
                    if tag['Key'] == 'Name':
                        name = tag['Value']

                if name:
                    severity = 0
                    message = 'Instance has a Name tag of {}'.format(
                        name
                    )
                else:
                    severity = 1
                    message = 'Instance does not have a Name tag'

                self.results.append({
                    'resource': instance_id,
                    'region': region,
                    'severity': severity,
                    'message': message
                })

        return self.results
