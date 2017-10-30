class Refinery(Refinery):
    """ Interface for higher level abstractions over boto3
    """

    required_clients = []

    def __init__(self, clients):
        self.clients = clients
