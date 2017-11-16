from setuptools import setup, find_packages

version = __import__('oil').version()

# For future package excludes, such as 'oil.config'
EXCLUDES = []

setup(
    name="oil",
    version=version,
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
