# TotalUsersPlugin


## Configurable Options

### Total Users Severity 2 Threshold
```python
'total_users_severity_2_threshold': {
    'name': 'Total Users Severity 2 Threshold',
    'description': (
        'Adjust threshold for number of users for a severity 2 finding'
    ),
    'value_description': 'number of users',
    'default': 1000,
}
```

### Total Users Severity 1 Threshold
```python
'total_users_severity_1_threshold': {
    'name': 'Total Users Severity 1 Threshold',
    'description': (
        'Adjust threshold for number of users for a severity 1 finding'
    ),
    'value_description': 'number of users',
    'default': 500,
}
```

### Total Users Severity 2 Message
```python
'total_users_severity_2_message': {
    'name': 'Total Users Severity 2 Message',
    'description': (
        'Change the message for a severity 2 finding'
    ),
    'value_description': '{total_users}',
    'default': 'There are {total_users} users for this account',
}
```

### Total Users Severity 1 Message
```python
'total_users_severity_1_message': {
    'name': 'Total Users Severity 1 Message',
    'description': (
        'Change the message for a severity 1 finding'
    ),
    'value_description': '{total_users}',
    'default': 'There are {total_users} users for this account',
}
```

### Total Users Severity 0 Message
```python
'total_users_severity_0_message': {
    'name': 'Total Users Severity 0 Message',
    'description': (
        'Change the message for a severity 0 finding'
    ),
    'value_description': '{total_users}',
    'default': 'There are {total_users} users for this account',
}
```

### No Users Message
```python
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
}
```

## Example Configuration
```Python
config = {
    'aws': {
        'iam': {
            'plugins': [
                {
                    'name': 'total_users',
                    'config': {
                        'total_users_severity_2_threshold': 50,
                        'total_users_severity_1_threshold': 20,
                        'total_users_severity_2_message': (
                            'Total users: {total_users}'
                        ),
                        'total_users_severity_1_message': (
                            'Total users: {total_users}'
                        ),
                        'total_users_severity_0_message': (
                            'Total users: {total_users}'
                        ),
                        'no_users_message': (
                            'No users in this AWS account'
                        ),
                    }
                }
            ]
        }
    }
}
oil = Oil(config)
results = oil.scan()
```
