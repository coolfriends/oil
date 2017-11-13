# AccessKeyUsagePlugin

## Configurable options
### access_key_last_used_severity_two_threshold
The threshold in days for a severity two finding.

### access_key_last_used_severity_one_threshold
The threshold in days for a severity one finding.

```Python
config = {
    'aws': {
        'iam': {
            'plugins': [
                {
                    'name': 'access_key_usage',
                    'config': {
                        'access_key_last_used_severity_two_threshold': 60,
                        'access_key_last_used_severity_one_threshold': 30,
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
