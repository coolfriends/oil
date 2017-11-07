from oil.plugins.aws.cloudfront import TLSProtocolPlugin
from oil.barrels.aws import CloudFrontBarrel


class Oil():
    def __init__(self, config={}):
        """
        TODO: Create sensible default configuration
        """
        self.config = config;
        self.plugins = []
        self.cached_api_data = {}
        self.scan_data = {}

        self._load_plugins()

    def _load_plugins(self):
        """
        TODO: Make adding plugins more dynamic than a large if statement
        """
        aws_config = self.config.get('aws', {})
        cloudfront_config = aws_config.get('cloudfront', {})


        for plugin in cloudfront_config.get('plugins', []):
            if plugin.get('name', '') == 'tls_protocol':
                configured_plugin = TLSProtocolPlugin(
                    plugin.get('config', {})
                )
                self.plugins.append(configured_plugin)

    def _collect_all_api_data(self):
        unique_api_calls = self._unique_api_calls()
        for provider, services in unique_api_calls.items():
            for service, api_calls in services.items():
                for api_call in api_calls:
                    self._collect_api_data(provider, service, api_call)


    def _collect_api_data(self, provider, service, call):
        if provider == 'aws':
            if not self.cached_api_data.get('aws'):
                self.cached_api_data['aws'] = {}

            aws_data = self.cached_api_data['aws']
            if service == 'cloudfront':
                if not aws_data.get('cloudfront'):
                    aws_data['cloudfront'] = {}

                cloudfront_data = aws_data['cloudfront']
                region = 'aws-global'
                if not cloudfront_data.get(region, {}):
                    cloudfront_data[region] = {}

                barrel = CloudFrontBarrel()
                data = barrel.tap(call)
                self.cached_api_data[provider][service][region][call] = data


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


    def scan(self):
        self._collect_all_api_data()
        self._run_plugins()
        # Return a copy of this so the user does not get direct access to saved scan results
        return self.scan_data.copy()
