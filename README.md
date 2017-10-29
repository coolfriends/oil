oil
====

An extensible cloud security analysis tool

## Goals
This project is based on some specific design goals:
* Written in Python
* Covers best practices by default for cloud services
* Provides a reference for justifcation/support for best practices
* Implements plugins that cover best practices for all AWS services available to boto3
* Enables users to configure varios aspects of plugins at runtime (specific to each plugin)
* Enables users to easily design new plugins
* Results are returned in a simple to navigate Python dictionary
* Support for Azure and Google Cloud

## Contributing
Create your branch with a descriptive name, create a virtual env, and download dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

Run the tests
```bash
invoke test
```
