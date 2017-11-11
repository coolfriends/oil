from oil.plugins.aws.cloudfront import TLSProtocolPlugin
from oil.plugins.aws.cloudfront import HTTPSPlugin
from oil.plugins.aws.cloudfront import S3OriginAccessIdentityPlugin
from oil.plugins.aws.ec2 import InstanceNameTagPlugin
from oil.plugins.aws.ec2 import PublicIpPlugin
from oil.barrels.aws import CloudFrontBarrel
from oil.barrels.aws import EC2Barrel

class Oil():
    default_config = {
        'aws': {
            'cloudfront': {
                'plugins': [
                    {
                        'name': 'tls_protocol',
                    },
                    {
                        'name': 'https'
                    },
                    {
                        'name': 's3_origin_access_identity'
                    }
                ]
            },
            'ec2': {
                'plugins': [
                    {
                        'name': 'instance_name_tag',
                    },
                    {
                        'name': 'public_ip',
                    }
                ]
            }
        }
    }

    supports = {
        'aws': {
            'cloudfront': {
                'tls_protocol': TLSProtocolPlugin,
                'https': HTTPSPlugin,
                's3_origin_access_identity': S3OriginAccessIdentityPlugin,
            },
            'ec2': {
                'instance_name_tag': InstanceNameTagPlugin,
                'public_ip': PublicIpPlugin
            }
        }
    }

    available_barrels = {
        'aws': {
            'cloudfront': CloudFrontBarrel,
            'ec2': EC2Barrel,
        }
    }

    def __init__(self, config={}):
        """
        TODO: Create sensible default configuration
        """
        self.config = config or self.default_config;
        self.cached_api_data = {}
        self.scan_data = {}
        self.plugins = []
        self._load_plugins()

    def scan(self):
        self._collect_all_api_data()
        self._run_plugins()

        # Return a copy of this so the user does not get
        # direct access to saved scan results
        return self.scan_data.copy()

    def configure(self, config):
        self.config = config
        self._load_plugins()

    @property
    def providers(self):
        return list(self.config.keys())

    def services(self, provider):
        services_dict = self.config.get(provider, {})
        services = [k for k in services_dict.keys()]
        if not services:
            message = 'Not configured for provider: {}'.format(provider)
            raise RuntimeError(message)

        return services

    def _supported_providers(self):
        return list(self.supports.keys())

    def _supported_services(self, provider):
        services = self.supports.get(provider, {})

        return list(services.keys())

    def _fetch_plugin(self, **kwargs):
        provider = kwargs['provider']
        service = kwargs['service']
        plugin_name = kwargs['plugin_name']
        return self.supports[provider][service][plugin_name]

    def _load_plugins(self):
        """
        TODO: Make adding plugins more dynamic than a large if statement
        TODO: Log if no plugins are passed in
        """
        self.plugins = []
        for provider, services in self.config.items():
            if provider not in self._supported_providers():
                raise RuntimeError('Unsupported provider: {}'.format(provider))

            for service, service_config in services.items():
                if service not in self._supported_services(provider):
                    message = 'Unsupported service: {}'.format(service)
                    raise RuntimeError()

                for plugin in service_config.get('plugins', []):
                    plugin_name = plugin.get('name', '')
                    try:
                        class_name = self._fetch_plugin(
                            provider=provider,
                            service=service,
                            plugin_name=plugin_name,
                        )
                    except KeyError as e:
                        message = 'Unsupported plugin: {}'.format(plugin_name)
                        raise RuntimeError(message) from e
                    configured_plugin = class_name(plugin.get('config', {}))

                    self.plugins.append(configured_plugin)

    def _collect_all_api_data(self):
        unique_api_calls = self._unique_api_calls()
        for provider, services in unique_api_calls.items():
            for service, api_calls in services.items():
                for api_call in api_calls:
                    self._collect_api_data(provider, service, api_call)

    def get_barrel(self, provider, service):
        for provider_name, services in self.available_barrels.items():
            for service_name, barrel in services.items():
                if provider == provider_name:
                    if service == service_name:
                        return barrel

        message = 'Barrel does not exist for Provider: {} Service: {}'.format(
            provider,
            service,
            )

        raise RuntimeError(message)

    def _collect_api_data(self, provider, service, call):
        if provider == 'aws':
            if not self.cached_api_data.get('aws'):
                self.cached_api_data['aws'] = {}

            aws_data = self.cached_api_data['aws']
            # barrel = self.get_barrel(provider, service)

            if service == 'cloudfront':
                if not aws_data.get('cloudfront'):
                    aws_data['cloudfront'] = {}

                cloudfront_data = aws_data['cloudfront']
                barrel = CloudFrontBarrel()
                data_by_region = barrel.tap(call)

                for region, call_data in data_by_region.items():
                    if not cloudfront_data.get(region, {}):
                        cloudfront_data[region] = {}
                    cloudfront_data[region][call] = call_data

            elif service == 'ec2':
                if not aws_data.get('ec2'):
                    aws_data['ec2'] = {}

                ec2_data = aws_data['ec2']

                barrel = EC2Barrel()
                data_by_region = barrel.tap(call)

                # Put calls in correct region
                for region, call_data in data_by_region.items():
                    if not ec2_data.get(region, {}):
                        ec2_data[region] = {}
                    ec2_data[region][call] = call_data
        else:
            raise RuntimeError(
                'This nested call {}:{}:{} is not implemented.'.format(
                    provider, service, call
                )
            )

    def _unique_api_calls(self):
        unique_api_calls = {}
        for plugin in self.plugins:
            for provider, services in plugin.required_api_calls.items():
                if provider not in unique_api_calls.keys():
                    unique_api_calls[provider] = {}

                for service, api_calls in services.items():
                    if service not in unique_api_calls[provider].keys():
                        unique_api_calls[provider][service] = set()

                    for api_call in api_calls:
                        unique_api_calls[provider][service].add(api_call)
        return unique_api_calls

    def _run_plugins(self):
        for plugin in self.plugins:
            results = plugin.run(self.cached_api_data)
            self._store_results(plugin, results)

    def _store_results(self, plugin, results):
        provider = plugin.provider
        service = plugin.service
        plugin_name = plugin.name

        if not self.scan_data.get(provider):
            self.scan_data[provider] = {}
        provider_data = self.scan_data[provider]

        if not provider_data.get(service):
            provider_data[service] = {}

        service_data = provider_data[service]
        service_data[plugin_name] = results
