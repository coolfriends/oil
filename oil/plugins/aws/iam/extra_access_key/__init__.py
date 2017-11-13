from oil.plugins import Plugin


class ExtraAccessKeyPlugin(Plugin):

    name = 'extra_access_key'
    provider = 'aws'
    service = 'iam'

    requirements = {
        'users': ['aws', 'iam', 'get_credential_report']
    }

    def run(self, api_data):
        # Reset the results list for this plugin
        self.results = []

        requirements = self.collect_requirements(api_data)
        users = requirements['users']['aws-global']

        if not users:
            self.results.append({
                'resource': 'None',
                'region': 'aws-global',
                'severity': 0,
                'message': 'No users found'
            })

        for user in users:
            username = user['user']
            resource_arn = user['arn']
            active_1 = user.get('access_key_1_active', 'false')
            active_2 = user.get('access_key_2_active', 'false')

            if active_1 == 'true' and active_2 == 'true':
                severity = 2
                message = 'Multiple active keys found for user {}'.format(
                    username,
                    )
            elif active_1 == 'true':
                severity = 0
                message = 'Key 1 active for user {}'.format(
                    username,
                )
            elif active_2 == 'true':
                severity = 0
                message = 'Key 2 active for user {}'.format(
                    username,
                )
            else:
                severity = 0
                message = 'No active keys for user {}'.format(
                    username,
                )

            self.results.append({
                'resource': resource_arn,
                'region': 'aws-global',
                'severity': severity,
                'message': message
            })

        return self.results
