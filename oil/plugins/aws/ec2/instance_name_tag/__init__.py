class InstanceNameTagPlugin():

    name = 'instance_name_tag'
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

                results.append({
                    'resource': instance_id,
                    'region': region,
                    'severity': severity,
                    'message': message
                })

        return results
