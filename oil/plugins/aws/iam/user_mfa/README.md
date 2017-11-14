# UserMFAPlugin

## Configurable options
### enabled_message
The message attached to a finding when MFA is enabled.
One may include {username} in the message format to access the username.

### not_enabled_message
The message attached to a finding when MFA is not enabled.
One may include {username} in the message format to access the username.

### not_enabled_severity_level
The severity level for a finding of MFA not enabled.
This value should be 0, 1, or 2.

```Python
config = {
    'aws': {
        'iam': {
            'plugins': [
                {
                    'name': 'user_mfa',
                    'config': {
                        'enabled_message': '{username} has MFA',
                        'not_enabled_message': '{username} doesn't have MFA,
                        'not_enabled_severity_level': 1
                    }
                }
            ]
        }
    }
}
oil = Oil(config)
results = oil.scan()
```


## Todo
* Add configurable messages for severity 0, 1, and 2
