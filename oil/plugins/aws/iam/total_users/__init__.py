from oil.plugins import Plugin


class TotalUsersPlugin(Plugin):

    name = 'total_users'
    provider = 'aws'
    service = 'iam'

    requirements = {
        'users': ['aws', 'iam', 'get_credential_report']
    }

    default_config = {
        'total_users_severity_2_threshold': {
            'name': 'Total Users Severity 2 Threshold',
            'description': (
                'Adjust threshold for number of users for a severity 2 finding'
            ),
            'value_description': 'number of users',
            'default': 1000,
        },
        'total_users_severity_1_threshold': {
            'name': 'Total Users Severity 1 Threshold',
            'description': (
                'Adjust threshold for number of users for a severity 1 finding'
            ),
            'value_description': 'number of users',
            'default': 500,
        },
        'total_users_severity_2_message': {
            'name': 'Total Users Severity 2 Message',
            'description': (
                'Change the message for a severity 2 finding'
            ),
            'value_description': '{total_users}',
            'default': 'There are {total_users} users for this account',
        },
        'total_users_severity_1_message': {
            'name': 'Total Users Severity 1 Message',
            'description': (
                'Change the message for a severity 1 finding'
            ),
            'value_description': '{total_users}',
            'default': 'There are {total_users} users for this account',
        },
        'total_users_severity_0_message': {
            'name': 'Total Users Severity 0 Message',
            'description': (
                'Change the message for a severity 0 finding'
            ),
            'value_description': '{total_users}',
            'default': 'There are {total_users} users for this account',
        },
        'no_users_message': {
            'name': 'No Users Message',
            'description': (
                'Change the message for no users for an account'
            ),
            'value_description': (
                'This should not be possible because of root account, but '
                'it may come in handy later'
            ),
            'default': 'There are no users for this account',
        },
    }


    def run(self, api_data):
        # Reset the results list for this plugin
        self.results = []

        requirements = self.collect_requirements(api_data)
        users = requirements['users']['aws-global']

        resource = 'None'
        region = 'aws-global'
        total_users = len(users)
        if not total_users:
            severity = 0
            message = self.config['no_users_message']
        elif total_users > self.config['total_users_severity_2_threshold']:
            severity = 2
            message = self.config['total_users_severity_2_message'].format(
                total_users=total_users,
            )
        elif total_users > self.config['total_users_severity_1_threshold']:
            severity = 1
            message = self.config['total_users_severity_1_message'].format(
                total_users=total_users,
            )
        else:
            severity = 0
            message = self.config['total_users_severity_0_message'].format(
                total_users=total_users,
            )

        self.results.append({
            'resource': resource,
            'region': region,
            'severity': severity,
            'message': message,
        })

        return self.results
