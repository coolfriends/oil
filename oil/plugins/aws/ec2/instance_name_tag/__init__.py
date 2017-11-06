class InstanceNameTagPlugin():
    def run(self, data):
        """
        data is of the form: {
          'us-east-1': [
             ... #Instances
          ],
          'us-east-2': [
             ... #Instances
          ]...
          # Other regions
        }
        TODO: Update to new documentation format
        TODO: Allow user to configure this plugin to use custom tag for Name
              (incase the user has a system set up where they use InstanceName,
               or even InStaNcE NAMe)
        """
        results = []

        for region, region_data in data.items():
            if not region_data:
                results.append({
                    'resource': 'None',
                    'region': region,
                    'severity': 0,
                    'message': 'No instances found'
                })

            for instance in region_data:
                instance_id = instance['InstanceId']
                tags = instance.get('Tags', [])
                name = None
                for tag in tags:
                    if tag['Key'] == 'Name':
                        name = tag['Value']

                if name:
                    severity = 0
                    message = 'Instance has instance name of {}'.format(
                        name
                    )
                else:
                    severity = 1
                    message = 'Instance does not have an instance tag'

                results.append({
                    'resource': instance_id,
                    'region': region,
                    'severity': severity,
                    'message': message
                })

        return results
