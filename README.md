oil
====
[![Build Status](https://travis-ci.org/coolfriends/oil.svg?branch=master)](https://travis-ci.org/coolfriends/oil)
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

Run without functional tests
```bash
invoke test --no-functional
```

Note: Running tests sets the OIL_FUNCTIONAL_TESTS env variable in your shell.



## Todo
* Decide on documentation format and write documentation using that format
* Write an invoke command to build documentation & clean up if necessary 
  (just google it)
* Write tests that cover as many potential inputs as possible. Specifically
  for plugins and edge cases for integrations tests (API call errors, etc)

