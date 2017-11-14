from oil.plugins.aws.cloudfront import *
from oil.plugins.aws.ec2 import *
from oil.plugins.aws.iam import *
from oil.barrels.aws import CloudFrontBarrel
from oil.barrels.aws import EC2Barrel
from oil.barrels.aws import IAMBarrel

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
            },
            'iam': {
                'plugins': [
                    {
                        'name': 'extra_access_key',
                    },
                    {
                        'name': 'access_key_usage',
                    },
                    {
                        'name': 'user_mfa',
                    },
                    {
                        'name': 'user_password_rotation',
                    },
                ]
            },
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
                'public_ip': PublicIpPlugin,
            },
            'iam': {
                'extra_access_key': ExtraAccessKeyPlugin,
                'access_key_usage': AccessKeyUsagePlugin,
                'user_mfa': UserMFAPlugin,
                'user_password_rotation': UserPasswordRotationPlugin,
            },
        },
    }

    available_barrels = [
        CloudFrontBarrel,
        EC2Barrel,
        IAMBarrel,
    ]

    def __init__(self, config={}):
        """
        TODO: Create sensible default configuration
        """
        self.config = config or self.default_config;
        self.cached_api_data = {}
        self.scan_data = {}
        self.plugins = []
        self._load_plugins()
        self._load_barrels()

    def scan(self):
        self._collect_all_api_data()
        self._run_plugins()

        # Return a copy of this so the user does not get
        # direct access to saved scan results
        return self.scan_data.copy()

    def configure(self, config):
        self.config = config
        self._load_plugins()
        self._load_barrels()

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

    def _load_barrels(self):
        self.barrels = []
        unique_service = set()
        for plugin in self.plugins:
            unique_service.add(
                (
                    plugin.provider,
                    plugin.service,
                )
            )

        for (provider, service) in unique_service:
            found = False
            for barrel in self.available_barrels:
                if provider == barrel.provider and service == barrel.service:
                    self.barrels.append(barrel())
                    found = True
            if not found:
                message = (
                    'Barrel not found for: Provider {}, Service {}'.format(
                        provider,
                        service,
                    )
                )
                raise RuntimeError(message)

    def _collect_all_api_data(self):
        unique_api_calls = self._unique_api_calls()
        for provider, services in unique_api_calls.items():
            for service, api_calls in services.items():
                for api_call in api_calls:
                    self._collect_api_data(provider, service, api_call)

    def get_barrel(self, provider, service):
        for barrel in self.barrels:
            if provider == barrel.provider:
                if service == barrel.service:
                    return barrel

        message = 'Barrel does not exist for Provider: {} Service: {}'.format(
            provider,
            service,
        )

        raise RuntimeError(message)

    def _collect_api_data(self, provider, service, call):
        if not self.cached_api_data.get(provider):
            self.cached_api_data[provider] = {}

        provider_data = self.cached_api_data[provider]

        if not provider_data.get(service):
            provider_data[service] = {}

        service_data = provider_data[service]
        barrel = self.get_barrel(provider, service)
        data_by_region = barrel.tap(call)

        for region, call_data in data_by_region.items():
            if not service_data.get(region, {}):
                service_data[region] = {}
            service_data[region][call] = call_data

    def _unique_api_calls(self):
        unique_api_calls = {}
        for plugin in self.plugins:
            for requirement, [provider, service, call] in plugin.requirements.items():
                if provider not in unique_api_calls.keys():
                    unique_api_calls[provider] = {}

                if service not in unique_api_calls[provider].keys():
                    unique_api_calls[provider][service] = set()

                unique_api_calls[provider][service].add(call)
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
