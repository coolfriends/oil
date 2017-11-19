

class Oil():
    _valid_kwargs = set([
        'aws_access_key_id',
        'aws_secret_access_key',
        'session_token'
    ])

    def __init__(self, config={}, **kwargs):
        """
        TODO: Create sensible default configuration
        """
        self._validate_kwargs(**kwargs)
        self.config = config
        self.cached_api_data = {}
        self.scan_data = {}
        self.plugins = {}
        self.barrels = {}
        self.unique_api_calls = {}
        self.aws_access_key_id = kwargs.get('aws_access_key_id')
        self.aws_secret_access_key = kwargs.get('aws_secret_access_key')
        self.session_token = kwargs.get('session_token')

    def register_barrel(self, barrel_cls, config={}):
        """ Register a barrel by provider and service name. It returns a
        reference to the instance of the barrel that is created in the
        registration process. A reference to the current :class:`Oil` instance
        is passed into the barrel instance.

        :param barrel_cls: the class name of a barrel

        :param config:     configuration for the barrel. see the documentation
                           on the barrel for information about configuration
                           options

        :returns a reference to the barrel instance created during registration

        """
        provider = barrel_cls.provider
        service = barrel_cls.service
        if self.get_barrel(provider, service):
            raise RuntimeError('Barrel {} - {} already exists.'.format(
                provider,
                service,
            ))

        # Make sure provider dict exists
        if not self.barrels.get(provider):
            self.barrels[provider] = {}

        self.barrels[provider][service] = barrel_cls(self, config=config)
        return self.barrels[provider][service]

    def register_plugin(self, plugin_cls, config={}):
        """ Register a plugin by provider, service, and plugin name. It returns
        a reference to the instance of the plugin that is created in the
        registration process. A reference to the current :class:`Oil` instance
        is passed into the plugin instance.

        :param plugin_cls: the class name of a plugin

        :param config:     configuration for the plugin. see the documentation
                           on the plugin for information about configuration
                           options

        :returns a reference to the plugin instance created during registration

        """
        provider = plugin_cls.provider
        service = plugin_cls.service
        plugin_name = plugin_cls.name
        if self.get_plugin(provider, service, plugin_name):
            raise RuntimeError('Plugin {} - {} - {} already exists.'.format(
                provider,
                service,
                plugin_name,
            ))

        # Make sure provider dict exists
        if not self.plugins.get(provider):
            self.plugins[provider] = {}

        # Make sure service dict exists
        if not self.plugins[provider].get(service):
            self.plugins[provider][service] = {}

        self.plugins[provider][service][plugin_name] = plugin_cls(self, config)
        return self.plugins[provider][service][plugin_name]

    def _validate_kwargs(self, **kwargs):
        for k, v in kwargs.items():
            if k not in self._valid_kwargs:
                raise RuntimeError(
                    'Received invalid kwarg: {}'.format(k)
                )

    def scan(self):
        self._collect_all_api_data()
        self._run_plugins()
        return self.scan_data

    def _collect_all_api_data(self):
        unique_api_calls = self._unique_api_calls()
        for provider, services in unique_api_calls.items():
            for service, api_calls in services.items():
                for api_call in api_calls:
                    self._collect_api_data(provider, service, api_call)

    def get_barrel(self, provider, service):
        """ Returns a reference to a barrel, or None
        """
        return self.barrels.get(provider, {}).get(service)

    def get_plugin(self, provider, service, name):
        """ Returns a reference to a plugin, or None
        """
        return self.plugins.get(provider, {}).get(service, {}).get(name)

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

    def _add_to_unique_api_calls(self, api_calls, plugin):
        for _, [provider, service, call] in plugin.requirements.items():
            if not api_calls.get(provider):
                api_calls[provider] = {}

            if not api_calls[provider].get(service):
                api_calls[provider][service] = set()

            api_calls[provider][service].add(call)

    def _unique_api_calls(self):
        unique_api_calls = {}
        for provider, services in self.plugins.items():
            for service, plugin_instances in services.items():
                for plugin_name, plugin in plugin_instances.items():
                    self._add_to_unique_api_calls(unique_api_calls, plugin)
        return unique_api_calls

    def _run_plugins(self):
        for provider, services in self.plugins.items():
            for service, plugin_instances in services.items():
                for plugin_name, plugin in plugin_instances.items():
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
