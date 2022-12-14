import asyncio
from typing import Any, Callable, Dict, List, Optional, cast

from aiohttp import ClientWebSocketResponse, WSMsgType

from binance4py.resources import Resource
from binance4py.typing import JsonObject

WEBSOCKET_URL = "wss://stream.binance.{}:443/stream"
WEBSOCKET_TEST_URL = "wss://testnet.binance.vision/stream"


class Websocket(Resource):
    __slots__ = [
        "_websocket_url",
        "_conn",
        "_exception",
        "_open_event",
        "_close_event",
        "_rate_limit",
        "_listeners",
        "_stream_callbacks",
        "_last_id",
        "_listen_key",
    ]

    def __init__(self, client) -> None:
        super().__init__(client)
        self._websocket_url = (
            WEBSOCKET_URL.format(self._client._tld)
            if not self._client._testnet
            else WEBSOCKET_TEST_URL
        )

        self._conn: Optional[ClientWebSocketResponse] = None
        self._exception: Optional[BaseException] = None
        self._open_event = asyncio.Event()
        self._close_event = asyncio.Event()

        self._rate_limit = asyncio.Semaphore(5)  # rps
        self._listeners: Dict[int, asyncio.Future] = {}
        self._stream_callbacks: Dict[str, List[Callable]] = {}
        self._last_id = 1

        self._listen_key: Optional[str] = None

    @property
    def closed(self) -> bool:
        return self._conn is None

    async def create_listen_key(self) -> str:
        return (
            await self._client.request(
                method="POST",
                url=self._client._api_url + self._client._endpoints.create_listen_key,
            )
        )["listenKey"]

    async def keep_alive_listen_key(self, listen_key: str) -> None:
        await self._client.request(
            method="PUT",
            url=self._client._api_url + self._client._endpoints.keep_alive_listen_key,
            params={"listenKey": listen_key},
        )

    async def close_listen_key(self, listen_key: str) -> None:
        await self._client.request(
            method="DELETE",
            url=self._client._api_url + self._client._endpoints.close_listen_key,
            params={"listenKey": listen_key},
        )

    async def _send(
        self, method: str, params: Optional[List[Any]] = None
    ) -> JsonObject:
        if self.closed:
            raise Exception("Websocket connection is closed")

        async with self._rate_limit:
            if self._rate_limit.locked():
                await asyncio.sleep(1)

            d = {"method": method, "id": self._last_id}
            self._last_id += 1

            if params is not None:
                d["params"] = params

            future = asyncio.get_running_loop().create_future()
            self._listeners[cast(int, d["id"])] = future

            await self._conn.send_json(  # type:ignore
                data=d, dumps=self._client._json_dumps
            )

            return await asyncio.wait_for(future, 10)

    async def subscribe(self, stream: str) -> JsonObject:
        return await self._send("SUBSCRIBE", [stream])

    async def subscribe_callback(self, stream: str, callback: Callable) -> None:
        if stream not in self._stream_callbacks:
            await self.subscribe(stream)

            self._stream_callbacks[stream] = [callback]
        else:
            self._stream_callbacks[stream].append(callback)

    async def unsubscribe(self, stream: str) -> JsonObject:
        return await self._send("UNSUBSCRIBE", [stream])

    async def unsubscribe_callback(self, stream: str, callback: Callable) -> None:
        if stream in self._stream_callbacks:
            if len(self._stream_callbacks[stream]) <= 1:
                await self.unsubscribe_all_callbacks(stream)
            else:
                try:
                    self._stream_callbacks[stream].remove(callback)
                except ValueError:
                    pass

    async def unsubscribe_all_callbacks(self, stream: str) -> None:
        await self.unsubscribe(stream)
        if stream in self._stream_callbacks:
            self._stream_callbacks.pop(stream)

    async def subscriptions(self) -> List[str]:
        return (await self._send("LIST_SUBSCRIPTIONS"))["result"]

    async def aggregate_trade(self, callback: Callable, symbol: str) -> str:
        stream = f"{symbol.lower()}@aggTrade"
        await self.subscribe_callback(stream, callback)
        return stream

    async def trade(self, callback: Callable, symbol: str) -> str:
        stream = f"{symbol.lower()}@trade"
        await self.subscribe_callback(stream, callback)
        return stream

    async def kline(self, callback: Callable, symbol: str, interval: str) -> str:
        stream = f"{symbol.lower()}@kline_{interval}"
        await self.subscribe_callback(stream, callback)
        return stream

    async def mini_ticker(self, callback: Callable, symbol: str) -> str:
        stream = f"{symbol.lower()}@miniTicker"
        await self.subscribe_callback(stream, callback)
        return stream

    async def mini_tickers(self, callback: Callable) -> str:
        stream = "!miniTicker@arr"
        await self.subscribe_callback(stream, callback)
        return stream

    async def ticker(self, callback: Callable, symbol: str) -> str:
        stream = f"{symbol.lower()}@ticker"
        await self.subscribe_callback(stream, callback)
        return stream

    async def tickers(self, callback: Callable) -> str:
        stream = "!ticker@arr"
        await self.subscribe_callback(stream, callback)
        return stream

    async def window_ticker(
        self, callback: Callable, symbol: str, window_size: str
    ) -> str:
        stream = f"{symbol.lower()}@ticker_{window_size}"
        await self.subscribe_callback(stream, callback)
        return stream

    async def window_tickers(self, callback: Callable, window_size: str) -> str:
        stream = f"!ticker_{window_size}@arr"
        await self.subscribe_callback(stream, callback)
        return stream

    async def book_ticker(self, callback: Callable, symbol: str) -> str:
        stream = f"{symbol.lower()}@bookTicker"
        await self.subscribe_callback(stream, callback)
        return stream

    async def partial_depth(
        self, callback: Callable, symbol: str, levels: int, update_speed: int = 1000
    ) -> str:
        stream = f"{symbol.lower()}@depth{levels}@{update_speed}ms"
        await self.subscribe_callback(stream, callback)
        return stream

    async def depth(
        self, callback: Callable, symbol: str, update_speed: int = 1000
    ) -> str:
        stream = f"{symbol.lower()}@depth@{update_speed}ms"
        await self.subscribe_callback(stream, callback)
        return stream

    async def _keep_alive_user_stream(
        self, listen_key: str, interval: int = 1800
    ) -> None:
        while True:
            await asyncio.sleep(interval)
            await self.keep_alive_listen_key(listen_key)

    async def user_data(self, callback: Callable) -> str:
        if self._listen_key is None:
            self._listen_key = await self.create_listen_key()
            asyncio.ensure_future(self._keep_alive_user_stream(self._listen_key))
        await self.subscribe_callback(self._listen_key, callback)
        return self._listen_key

    def _handle_task_exception(self, f: asyncio.Task) -> None:
        if not f.cancelled():
            exp = f.exception()
            if exp is not None:
                self._exception = exp
                asyncio.create_task(self.stop())

    async def _starter(self) -> None:
        try:
            async with self._client._session.ws_connect(
                url=self._websocket_url, heartbeat=180
            ) as ws:
                self._conn = ws

                self._open_event.set()
                self._close_event.clear()

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
                                task = asyncio.create_task(callback(data["data"]))
                                task.add_done_callback(self._handle_task_exception)
        finally:
            self._last_id = 1
            self._listeners.clear()
            self._stream_callbacks.clear()

            self._close_event.set()
            self._open_event.clear()

    async def start(self) -> None:
        if not self.closed:
            return

        asyncio.ensure_future(self._starter())

        await self._open_event.wait()

    async def stop(self) -> None:
        if self.closed:
            return

        await self._conn.close()  # type:ignore

    async def wait_stop(self) -> None:
        if not self._close_event.is_set():
            await self._close_event.wait()
            if self._exception is not None:
                raise self._exception
