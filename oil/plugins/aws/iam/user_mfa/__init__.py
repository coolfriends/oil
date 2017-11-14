from oil.plugins import Plugin


class UserMFAPlugin(Plugin):

    name = 'user_mfa'
    provider = 'aws'
    service = 'iam'

    requirements = {
        'users': ['aws', 'iam', 'get_credential_report']
    }

    default_config = {
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
        users = requirements['users']['aws-global']

        if not users:
            self.results.append({
                'resource': 'None',
                'region': 'aws-global',
                'severity': 0,
                'message': 'No users found'
            })

        for user in users:
            # Root user has separate plugin
            if user['user'] == '<root_account>':
                continue

            username = user['user']
            resource_arn = user['arn']
            mfa_active = user.get('mfa_active', 'false')

            if mfa_active == 'true':
                severity = 0
                message = self.config['enabled_message'].format(
                    username=username,
                )
            else:
                severity = self.config['not_enabled_severity_level']
                message = self.config['not_enabled_message'].format(
                    username=username,
                )

            self.results.append({
                'resource': resource_arn,
                'region': 'aws-global',
                'severity': severity,
                'message': message
            })

        return self.results
