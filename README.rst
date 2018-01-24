oil
===
.. image:: https://travis-ci.org/coolfriends/oil.svg?branch=master
           :target: https://travis-ci.org/coolfriends/oil

Introduction
-------------
Oil is an extensible cloud security analysis tool.

Goals
-----
This project is based on some specific design goals:

- Written in Python
- Covers best practices by default for cloud services
- Provides a reference for justifcation/support for best practices
- Implements plugins that cover best practices for all AWS services available to boto3
- Enables users to configure varios aspects of plugins at runtime (specific to each plugin)
- Enables users to easily design new plugins
- Results are returned in a simple to navigate Python dictionary
- Support for Azure and Google Cloud
- Released on PyPI


Build
-----
Download the repo and install with::

  pip install -e .

Development Usage
-----------------
Run the default scan and print to console::

  oil

Specify csv output::

  oil --output csv

Save to file::

  oil -f myfile.json

Contributing
------------
Clone a copy and install locally::

  git clone https://github.com/your-fork/oil.git
  cd oil
  pip install -e .

Run the tests::

  invoke test

Run without functional tests::

  invoke test --no-functional

Note: Running tests sets the OIL_FUNCTIONAL_TESTS env variable in your shell.


Todo
----
- Decide on documentation format and write documentation using that format
- Write an invoke command to build documentation & clean up if necessary 
  (just google it)
