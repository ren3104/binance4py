from typing import List, Optional, Union

from binance4py.typing import JsonObject

from .base import Resource


class General(Resource):
    async def ping(self) -> None:
        await self._client.request(
            method="GET", url=self._client._api_url + self._client._endpoints.ping
        )

    async def server_time(self) -> int:
        return (
            await self._client.request(
                method="GET",
                url=self._client._api_url + self._client._endpoints.server_time,
            )
        )["serverTime"]

    async def exchange_info(
        self,
        symbols: Optional[Union[str, List[str]]] = None,
        permissions: Optional[Union[str, List[str]]] = None,
    ) -> JsonObject:
        if isinstance(symbols, str):
            symbols = [symbols]

        return await self._client.request(
            method="GET",
            url=self._client._api_url + self._client._endpoints.exchange_info,
            params={"symbols": symbols, "permissions": permissions},
        )
