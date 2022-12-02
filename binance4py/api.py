import json
from typing import Optional
from .client import Client
from .endpoints import Endpoints
from .typing import JsonDumper, JsonLoader
from .resources import *
from .websocket import Websocket


class Binance(Client):
    __slots__ = ["general", "market", "spot", "ws"]

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        endpoints: Endpoints = Endpoints(),
        tld: str = "com",
        cluster: Optional[int] = None,
        testnet: bool = False,
        # output_json: bool = False,
        json_dumps: JsonDumper = json.dumps,
        json_loads: JsonLoader = json.loads
    ) -> None:
        super().__init__(
            api_key,
            api_secret,
            endpoints,
            tld,
            cluster,
            testnet,
            # output_json,
            json_dumps,
            json_loads
        )

        self.general = General(self)
        self.market = Market(self)
        self.spot = Spot(self)
        self.ws = Websocket(self)
