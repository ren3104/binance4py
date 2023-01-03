import hashlib
import hmac
import json
from typing import Any, Dict, Optional
from urllib.parse import urlencode

from aiohttp import ClientSession, ContentTypeError

from binance4py.endpoints import Endpoints
from binance4py.exception import BinanceApiException
from binance4py.typing import JsonDumper, JsonLoader
from binance4py.utils import create_query_dict, get_timestamp

API_URL = "https://api{}.binance.{}/api/"
API_TEST_URL = "https://testnet.binance.vision/api/"


class Client:
    __slots__ = [
        "_api_key",
        "_api_secret",
        "_testnet",
        "_endpoints",
        "_tld",
        "_api_url",
        "_json_dumps",
        "_json_loads",
        "_session",
    ]

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        endpoints: Endpoints = Endpoints(),
        tld: str = "com",
        cluster: Optional[int] = None,
        testnet: bool = False,
        json_dumps: JsonDumper = json.dumps,
        json_loads: JsonLoader = json.loads,
    ) -> None:
        self._api_key = api_key
        self._api_secret = api_secret
        self._testnet = testnet

        self._endpoints = endpoints
        self._tld = tld
        self._api_url = (
            API_URL.format(cluster or "", self._tld) if not testnet else API_TEST_URL
        )

        self._json_dumps = json_dumps
        self._json_loads = json_loads

        headers = {"User-Agent": "binance4py", "Accept": "application/json"}
        if self._api_key:
            headers["X-MBX-APIKEY"] = self._api_key
        self._session = ClientSession(headers=headers, json_serialize=self._json_dumps)

    @property
    def closed(self) -> bool:
        return self._session.closed

    def _generate_signature(self, query: str) -> str:
        if self._api_secret is None:
            raise Exception("Api secret cannot be None")

        return hmac.new(
            self._api_secret.encode("utf-8"), query.encode("utf-8"), hashlib.sha256
        ).hexdigest()

    async def request(
        self,
        method: str,
        url: str,
        signed: bool = False,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        if params is not None:
            params = create_query_dict(params)

        if signed:
            if params is None:
                params = {}
            params["timestamp"] = get_timestamp()
            params["signature"] = self._generate_signature(urlencode(params))

        async with self._session.request(method, url, params=params) as response:
            if not response.ok:
                raise BinanceApiException(response, await response.text())

            try:
                return await response.json(loads=self._json_loads)
            except ContentTypeError:
                raise Exception(
                    f"Invalid response content type: {response.content_type}"
                )

    async def open(self) -> "Client":
        return self

    async def close(self) -> None:
        if self.closed:
            return
        await self._session.close()

    async def __aenter__(self) -> "Client":
        return await self.open()

    async def __aexit__(self, *args) -> None:
        await self.close()
