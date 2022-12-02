from .base import Resource
from ..typing import JsonObject
from typing import Optional, Union, List


class Market(Resource):
    async def order_book(self, symbol: str, limit: Optional[int] = None) -> JsonObject:
        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.order_book,
            params={
                "symbol": symbol,
                "limit": limit
            }
        )
    
    async def recent_trades(self, symbol: str, limit: Optional[int] = None) -> JsonObject:
        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.recent_trades,
            params={
                "symbol": symbol,
                "limit": limit
            }
        )
    
    async def old_trades(
        self,
        symbol: str,
        limit: Optional[int] = None,
        from_id: Optional[int] = None
    ) -> JsonObject:
        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.old_trades,
            params={
                "symbol": symbol,
                "limit": limit,
                "fromId": from_id
            }
        )
    
    async def aggregate_trades(
        self,
        symbol: str,
        from_id: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> JsonObject:
        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.aggregate_trades,
            params={
                "symbol": symbol,
                "fromId": from_id,
                "startTime": start_time,
                "endTime": end_time,
                "limit": limit
            }
        )
    
    async def klines(
        self,
        symbol: str,
        interval: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> JsonObject:
        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.klines,
            params={
                "symbol": symbol,
                "interval": interval,
                "startTime": start_time,
                "endTime": end_time,
                "limit": limit
            }
        )
    
    async def ui_klines(
        self,
        symbol: str,
        interval: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> JsonObject:
        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.ui_klines,
            params={
                "symbol": symbol,
                "interval": interval,
                "startTime": start_time,
                "endTime": end_time,
                "limit": limit
            }
        )
    
    async def average_price(self, symbol: str) -> JsonObject:
        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.average_price,
            params={"symbol": symbol}
        )
    
    async def ticker_24hr(
        self,
        symbols: Optional[Union[str, List[str]]] = None,
        type: Optional[str] = None
    ) -> JsonObject:
        if isinstance(symbols, str):
            symbols = [symbols]
        
        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.ticker_24hr,
            params={
                "symbols": symbols,
                "type": type
            }
        )
    
    async def price_ticker(self, symbols: Optional[Union[str, List[str]]] = None) -> JsonObject:
        if isinstance(symbols, str):
            symbols = [symbols]

        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.price_ticker,
            params={"symbols": symbols}
        )
    
    async def order_book_ticker(self, symbols: Optional[Union[str, List[str]]] = None) -> JsonObject:
        if isinstance(symbols, str):
            symbols = [symbols]

        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.order_book_ticker,
            params={"symbols": symbols}
        )
    
    async def rolling_window_ticker(
        self,
        symbols: Union[str, List[str]],
        window_size: Optional[str] = None,
        type: Optional[str] = None
    ) -> JsonObject:
        if isinstance(symbols, str):
            symbols = [symbols]
        
        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.rolling_window_ticker,
            params={
                "symbols": symbols,
                "windowSize": window_size,
                "type": type
            }
        )
