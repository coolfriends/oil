class Plugin():

    name = None
    provider = None
    service = None

    default_config = {}

    def __init__(self, oil, config={}):
        """ Base initalization

        :param oil: a reference to an :class:`Oil` instance

        :param config: the configuration for the plugin

        """
        self.oil = oil
        self.config = self.configure(config)
        self.results = []

    def configure(self, config):
        """ Generic method to merge default_config and config for a Plugin
        """
        merged_config = {}
        for k, v in self.default_config.items():
            # Use provided config, or revert to default
            merged_config[k] = config.get(k, v['default'])
        return merged_config

    def collect_requirements(self, api_data):
        collected_data = {}
        for requirement, [provider, service, call]  in self.requirements.items():
            collected_data[requirement] = {}
            provider_data = api_data.get(provider, {})
            if not provider_data:
                raise RuntimeError(
                    'Provider missing from collected data: {}'.format(provider)
                )

            service_data = provider_data.get(service, {})
            if not service_data:
                raise RuntimeError(
                    'Service missing from collected data: {}'.format(service)
                )

            for region, calls in service_data.items():
                call_data = calls.get(call)
                if call_data is None:
                    raise RuntimeError(
                        'API call missing from collected data: {}'.format(call)
                    )
                collected_data[requirement][region] = call_data

        return collected_data
