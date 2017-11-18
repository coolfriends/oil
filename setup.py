import re
from setuptools import setup, find_packages

# get the version as a string, assuming it's at the top of oil/__init__.py
version_reg = re.compile('\d.\d')
with open('oil/__init__.py') as f:
    match = version_reg.search(f.readline())
    _version = match[0]

# For future package excludes, such as 'oil.config'
EXCLUDES = []

setup(
    name="oil",
    version=_version,
    url="https://github.com/coolfriends/oil",
    author="Cabal",
    description='An extensible framework for auditing cloud resources.',
    license='MIT',
    packages=find_packages(exclude=EXCLUDES),
    install_requires=[
        'boto3',
        'arrow',
    ],
)
