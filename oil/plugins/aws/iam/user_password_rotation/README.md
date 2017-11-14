# UserPasswordRotationPlugin

## Configurable options
Note: all available format variables are not required

### password_rotation_severity_2_threshold
```python
'password_rotation_severity_2_threshold': {
    'name': 'Threshold for Password Rotation Severity 2',
    'description': 'Threshold for password age in days for severity 2',
    'value_description': 'number of days',
    'default': 365,
}
```

### password_rotation_severity_1_threshold
```python
'password_rotation_severity_1_threshold': {
    'name': 'Threshold for Password Rotation Severity 1',
    'description': 'Threshold for password age in days for severity 1',
    'value_description': 'number of days',
    'default': 180,
}
```

### password_rotation_severity_2_message
```python
'password_rotation_severity_2_message': {
    'name': 'Password Rotation Message for Severity 2 Finding',
    'description': 'The message displayed for a severity 2 finding',
    'value_description': '{username} {days}',
    'default': '{username} has not rotated their password in {days} days',
}
```

### password_rotation_severity_1_message
```python
'password_rotation_severity_1_message': {
    'name': 'Password Rotation Message for Severity 1 Finding',
    'description': 'The message displayed for a severity 1 finding',
    'value_description': '{username} {days}',
    'default': '{username} has not rotated their password in {days} days',
}
```

### password_rotation_severity_0_message
```python
'password_rotation_severity_0_message': {
    'name': 'Password Rotation Message for Severity 0 Finding',
    'description': 'The message displayed for a severity 0 finding',
    'value_description': '{username} {days}',
    'default': '{username} has not rotated their password in {days} days',
}
```

### no_password_message
```python
'no_password_message': {
    'name': 'No Password Message',
    'description': 'Message displayed when the user has no password',
    'value_description': '{username}',
    'default': '{username} does not have an AWS console password',
},
```


```Python
config = {
    'aws': {
        'iam': {
            'plugins': [
                {
                    'name': 'user_password_rotation',
                    'config': {
                        'password_rotation_severity_2_threshold': 180,
                        'password_rotation_severity_1_threshold': 90,
                        'password_rotation_severity_2_message': (
                            '{days} days since last rotation for {username} '
                        ),
                        'password_rotation_severity_1_message': (
                            '{days} days since last rotation for {username}'
                        ),
                        'password_rotation_severity_0_message': (
                            '{username} is not violating password rotation '
                            'best practices'
                        ),
                        'password_rotation_severity_0_message': (
                            'No password for this user'
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
