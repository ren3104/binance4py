import asyncio
from typing import Any, Callable, Dict, List, Optional, cast

from aiohttp import ClientWebSocketResponse, WSMsgType

from binance4py.resources import Resource
from binance4py.typing import JsonObject

WEBSOCKET_URL = "wss://stream.binance.{}:443/stream"


class Websocket(Resource):
    __slots__ = [
        "_WEBSOCKET_URL",
        "_ws_conn",
        "_rate_limit",
        "_listeners",
        "_stream_callbacks",
        "_last_id",
    ]

    def __init__(self, client) -> None:
        super().__init__(client)
        self._WEBSOCKET_URL = WEBSOCKET_URL.format(self._client._tld)

        self._ws_conn: Optional[ClientWebSocketResponse] = None
        self._rate_limit = asyncio.Semaphore(5)  # rps
        self._listeners: Dict[int, asyncio.Future] = {}
        self._stream_callbacks: Dict[str, List[Callable]] = {}
        self._last_id = 1

    @property
    def closed(self) -> bool:
        return self._ws_conn is None

    async def create_listen_key(self) -> str:
        return (
            await self._client.request(
                method="POST",
                url=self._client._API_URL + self._client._endpoints.create_listen_key,
            )
        )["listenKey"]

    async def keep_alive_listen_key(self, listen_key: str) -> None:
        await self._client.request(
            method="PUT",
            url=self._client._API_URL + self._client._endpoints.keep_alive_listen_key,
            params={"listenKey": listen_key},
        )

    async def close_listen_key(self, listen_key: str) -> None:
        await self._client.request(
            method="DELETE",
            url=self._client._API_URL + self._client._endpoints.close_listen_key,
            params={"listenKey": listen_key},
        )

    async def _send(
        self, method: str, params: Optional[List[Any]] = None
    ) -> JsonObject:
        if self.closed:
            raise Exception("Websocket connection is closed")

        async with self._rate_limit:
            d = {"method": method, "id": self._last_id}

            if params is not None:
                d["params"] = params

            future = asyncio.get_running_loop().create_future()
            self._listeners[cast(int, d["id"])] = future

            await self._ws_conn.send_json(  # type:ignore
                data=d, dumps=self._client._json_dumps
            )

            self._last_id += 1

            res = await asyncio.wait_for(future, 5)

            if self._rate_limit.locked():
                await asyncio.sleep(1)

        return res

    async def subscribe(self, stream: str, callback: Callable) -> None:
        if stream not in self._stream_callbacks:
            await self._send("SUBSCRIBE", [stream])

            self._stream_callbacks[stream] = [callback]
        else:
            self._stream_callbacks[stream].append(callback)

    async def unsubscribe(self, stream: str) -> None:
        await self._send("UNSUBSCRIBE", [stream])
        if stream in self._stream_callbacks:
            del self._stream_callbacks[stream]

    async def subscriptions(self) -> List[str]:
        return (await self._send("LIST_SUBSCRIPTIONS"))["result"]

    async def kline(self, callback: Callable, symbol: str, interval: str):
        await self.subscribe(f"{symbol}@kline_{interval}", callback)

    async def start(self) -> None:
        if not self.closed:
            return

        try:
            async with self._client._session.ws_connect(
                url=self._WEBSOCKET_URL, heartbeat=180
            ) as ws:
                self._ws_conn = ws

                async for msg in ws:
                    if msg.type == WSMsgType.TEXT:
                        data = msg.json(loads=self._client._json_loads)

                        if "error" in data:
                            raise Exception(
                                f"Websocket error code {data['error']['code']}. {data['error']['msg']}"
                            )
                        elif "id" in data and data["id"] in self._listeners:
                            future = self._listeners[data["id"]]
                            if not future.cancelled():
                                future.set_result(data)
                            self._listeners.pop(data["id"])
                        elif "stream" in data:
                            for callback in self._stream_callbacks[data["stream"]]:
                                await callback(data)
        finally:
            self._stream_callbacks.clear()

    async def stop(self) -> None:
        if self.closed:
            return

        self._ws_conn.close()  # type:ignore
