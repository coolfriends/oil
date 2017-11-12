class Plugin():

    def __init__(self, config={}):
        """
        TODO: Set up sensible default config
        TODO: Set up configurable variables
        """
        self.config = config
        self.results = []

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

            for region, calls  in service_data.items():
                call_data = calls.get(call)
                if call_data is None:
                    raise RuntimeError(
                        'API call missing from collected data: {}'.format(call)
                    )
                collected_data[requirement][region] = call_data

        return collected_data
