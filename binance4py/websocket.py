from .resources.base import Resource
from .typing import JsonObject
from aiohttp import WSMsgType
import asyncio
from typing import Dict, List, Callable


WEBSOCKET_URL = "wss://stream.binance.{}:443/stream"


class Websocket(Resource):
    __slots__ = [
        "_WEBSOCKET_URL",
        "_ws_conn",
        "_start_event",
        "_rate_limit",
        "_stream_callbacks",
        "_last_id"
    ]

    def __init__(self, client) -> None:
        super().__init__(client)
        self._WEBSOCKET_URL = WEBSOCKET_URL.format(self._client._tld)

        self._ws_conn = None
        self._start_event = asyncio.Event()
        self._rate_limit = asyncio.Semaphore(5) # rps
        self._stream_callbacks: Dict[str, List[Callable]] = {}
        self._last_id = 1
    
    @property
    def closed(self) -> bool:
        return self._ws_conn is None
    
    async def create_listen_key(self) -> str:
        return (await self._client.request(
            method="POST",
            url=self._client._API_URL + self._client._endpoints.create_listen_key
        ))["listenKey"]
    
    async def keep_alive_listen_key(self, listen_key: str) -> None:
        return await self._client.request(
            method="PUT",
            url=self._client._API_URL + self._client._endpoints.keep_alive_listen_key,
            params={
                "listenKey": listen_key
            }
        )
    
    async def close_listen_key(self, listen_key: str) -> None:
        return await self._client.request(
            method="DELETE",
            url=self._client._API_URL + self._client._endpoints.close_listen_key,
            params={
                "listenKey": listen_key
            }
        )

    async def _send(self, data: JsonObject) -> None:
        if self.closed:
            raise Exception("Websocket connection is closed")
        
        async with self._rate_limit:
            await self._ws_conn.send_json(
                data=data,
                dumps=self._client._json_dumps
            )

            if self._rate_limit.locked():
                await asyncio.sleep(1)
    
    async def subscribe(self, stream: str, callback: Callable) -> None:
        await self._start_event.wait()

        if stream not in self._stream_callbacks:
            await self._send({
                "method": "SUBSCRIBE",
                "params": [stream],
                "id": self._last_id
            })

            self._last_id += 1

            self._stream_callbacks[stream] = [callback]
        else:
            self._stream_callbacks[stream].append(callback)
    
    def kline(self, symbol: str, interval: str, callback: Callable):
        asyncio.ensure_future(self.subscribe(f"{symbol}@kline_{interval}", callback))
    
    async def start(self) -> None:
        if not self.closed:
            return
        
        try:
            async with self._client._session.ws_connect(
                url=self._WEBSOCKET_URL,
                heartbeat=180
            ) as ws:
                self._ws_conn = ws
                self._start_event.set()

                async for msg in ws:
                    if msg.type == WSMsgType.TEXT:
                        data = msg.json(loads=self._client._json_loads)
                        if "stream" in data:
                            for callback in self._stream_callbacks[data["stream"]]:
                                await callback(data)
        finally:
            self._stream_callbacks.clear()
            self._start_event.clear()
    
    async def stop(self) -> None:
        if self.closed:
            return

        self._ws_conn.close()
