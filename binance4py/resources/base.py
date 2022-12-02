from ..client import Client


class Resource:
    __slots__ = ["_client"]
    
    def __init__(self, client: Client) -> None:
        self._client = client
