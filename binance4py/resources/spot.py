from decimal import Decimal
from typing import Optional, Union
from .base import Resource
from ..typing import JsonObject


class Spot(Resource):
    async def create_test_order(
        self,
        symbol: str,
        side: str,
        type: str,
        time_in_force: Optional[str] = None,
        quantity: Optional[Union[int, float, Decimal]] = None,
        quote_order_qty: Optional[Union[int, float, Decimal]] = None,
        price: Optional[Union[int, float, Decimal]] = None,
        stop_price: Optional[Union[int, float, Decimal]] = None,
        new_client_order_id: Optional[str] = None,
        strategy_id: Optional[int] = None,
        strategy_type: Optional[int] = None,
        trailing_delta: Optional[int] = None,
        iceberg_qty: Optional[Union[int, float, Decimal]] = None,
        order_resp_type: Optional[str] = None
    ) -> JsonObject:
        return await self._client.request(
            method="POST",
            url=self._client._API_URL + self._client._endpoints.create_test_order,
            signed=True,
            params={
                "symbol": symbol,
                "side": side,
                "type": type,
                "timeInForce": time_in_force,
                "quantity": quantity,
                "quoteOrderQty": quote_order_qty,
                "price": price,
                "newClientOrderId": new_client_order_id,
                "strategyId": strategy_id,
                "strategyType": strategy_type,
                "stopPrice": stop_price,
                "trailingDelta": trailing_delta,
                "icebergQty": iceberg_qty,
                "newOrderRespType": order_resp_type
            }
        )
    
    async def create_order(
        self,
        symbol: str,
        side: str,
        type: str,
        time_in_force: Optional[str] = None,
        quantity: Optional[Union[int, float, Decimal]] = None,
        quote_order_qty: Optional[Union[int, float, Decimal]] = None,
        price: Optional[Union[int, float, Decimal]] = None,
        stop_price: Optional[Union[int, float, Decimal]] = None,
        new_client_order_id: Optional[str] = None,
        strategy_id: Optional[int] = None,
        strategy_type: Optional[int] = None,
        trailing_delta: Optional[int] = None,
        iceberg_qty: Optional[Union[int, float, Decimal]] = None,
        order_resp_type: Optional[str] = None
    ) -> JsonObject:
        return await self._client.request(
            method="POST",
            url=self._client._API_URL + self._client._endpoints.create_order,
            signed=True,
            params={
                "symbol": symbol,
                "side": side,
                "type": type,
                "timeInForce": time_in_force,
                "quantity": quantity,
                "quoteOrderQty": quote_order_qty,
                "price": price,
                "newClientOrderId": new_client_order_id,
                "strategyId": strategy_id,
                "strategyType": strategy_type,
                "stopPrice": stop_price,
                "trailingDelta": trailing_delta,
                "icebergQty": iceberg_qty,
                "newOrderRespType": order_resp_type
            }
        )
    
    async def cancel_order(
        self,
        symbol: str,
        order_id: Optional[int] = None,
        orig_client_order_id: Optional[str] = None,
        new_client_order_id: Optional[str] = None
    ) -> JsonObject:
        return await self._client.request(
            method="DELETE",
            url=self._client._API_URL + self._client._endpoints.cancel_order,
            signed=True,
            params={
                "symbol": symbol,
                "orderId": order_id,
                "origClientOrderId": orig_client_order_id,
                "newClientOrderId": new_client_order_id
            }
        )
    
    async def cancel_all_open_orders(self, symbol: str) -> JsonObject:
        return await self._client.request(
            method="DELETE",
            url=self._client._API_URL + self._client._endpoints.cancel_all_open_orders,
            signed=True,
            params={"symbol": symbol}
        )
    
    async def query_order(
        self,
        symbol: str,
        order_id: Optional[int] = None,
        orig_client_order_id: Optional[str] = None
    ) -> JsonObject:
        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.query_order,
            signed=True,
            params={
                "symbol": symbol,
                "orderId": order_id,
                "origClientOrderId": orig_client_order_id
            }
        )
    
    async def replace_order(
        self,
        symbol: str,
        side: str,
        type: str,
        cancel_replace_mode: str,
        time_in_force: Optional[str] = None,
        quantity: Optional[Union[int, float, Decimal]] = None,
        quote_order_qty: Optional[Union[int, float, Decimal]] = None,
        price: Optional[Union[int, float, Decimal]] = None,
        stop_price: Optional[Union[int, float, Decimal]] = None,
        cancel_new_client_order_id: Optional[str] = None,
        cancel_orig_client_order_id: Optional[str] = None,
        cancel_order_id: Optional[int] = None,
        new_client_order_id: Optional[str] = None,
        strategy_id: Optional[int] = None,
        strategy_type: Optional[int] = None,
        trailing_delta: Optional[int] = None,
        iceberg_qty: Optional[Union[int, float, Decimal]] = None,
        order_resp_type: Optional[str] = None
    ) -> JsonObject:
        return await self._client.request(
            method="POST",
            url=self._client._API_URL + self._client._endpoints.replace_order,
            signed=True,
            params={
                "symbol": symbol,
                "side": side,
                "type": type,
                "cancelReplaceMode": cancel_replace_mode,
                "timeInForce": time_in_force,
                "quantity": quantity,
                "quoteOrderQty": quote_order_qty,
                "price": price,
                "cancelNewClientOrderId": cancel_new_client_order_id,
                "cancelOrigClientOrderId": cancel_orig_client_order_id,
                "cancelOrderId": cancel_order_id,
                "newClientOrderId": new_client_order_id,
                "strategyId": strategy_id,
                "strategyType": strategy_type,
                "stopPrice": stop_price,
                "trailingDelta": trailing_delta,
                "icebergQty": iceberg_qty,
                "newOrderRespType": order_resp_type
            }
        )
    
    async def open_orders(self, symbol: Optional[str] = None) -> JsonObject:
        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.open_orders,
            signed=True,
            params={"symbol": symbol}
        )
    
    async def all_orders(
        self,
        symbol: str,
        order_id: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> JsonObject:
        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.all_orders,
            signed=True,
            params={
                "symbol": symbol,
                "orderId": order_id,
                "startTime": start_time,
                "endTime": end_time,
                "limit": limit
            }
        )
    
    async def create_oco_order(
        self,
        symbol: str,
        side: str,
        quantity: Union[int, float, Decimal],
        price: Union[int, float, Decimal],
        stop_price: Union[int, float, Decimal],
        list_client_order_id: Optional[str] = None,
        limit_client_order_id: Optional[str] = None,
        limit_strategy_id: Optional[int] = None,
        limit_strategy_type: Optional[int] = None,
        limit_iceberg_qty: Optional[Union[int, float, Decimal]] = None,
        trailing_delta: Optional[int] = None,
        stop_client_order_id: Optional[str] = None,
        stop_strategy_id: Optional[int] = None,
        stop_strategy_type: Optional[int] = None,
        stop_limit_price: Optional[Union[int, float, Decimal]] = None,
        stop_iceberg_qty: Optional[Union[int, float, Decimal]] = None,
        stop_limit_time_in_force: Optional[str] = None,
        new_order_resp_type: Optional[str] = None,
    ) -> JsonObject:
        return await self._client.request(
            method="POST",
            url=self._client._API_URL + self._client._endpoints.create_oco_order,
            signed=True,
            params={
                "symbol": symbol,
                "listClientOrderId": list_client_order_id,
                "side": side,
                "quantity": quantity,
                "limitClientOrderId": limit_client_order_id,
                "limitStrategyId": limit_strategy_id,
                "limitStrategyType": limit_strategy_type,
                "price": price,
                "limitIcebergQty": limit_iceberg_qty,
                "trailingDelta": trailing_delta,
                "stopClientOrderId": stop_client_order_id,
                "stopPrice": stop_price,
                "stopStrategyId": stop_strategy_id,
                "stopStrategyType": stop_strategy_type,
                "stopLimitPrice": stop_limit_price,
                "stopIcebergQty": stop_iceberg_qty,
                "stopLimitTimeInForce": stop_limit_time_in_force,
                "newOrderRespType": new_order_resp_type
            }
        )
    
    async def cancel_oco_order(
        self,
        symbol: str,
        order_list_id: Optional[int] = None,
        list_client_order_id: Optional[str] = None,
        new_client_order_id: Optional[str] = None
    ) -> JsonObject:
        return await self._client.request(
            method="DELETE",
            url=self._client._API_URL + self._client._endpoints.cancel_oco_order,
            signed=True,
            params={
                "symbol": symbol,
                "orderListId": order_list_id,
                "listClientOrderId": list_client_order_id,
                "newClientOrderId": new_client_order_id
            }
        )
    
    async def query_oco_order(
        self,
        order_list_id: Optional[int] = None,
        orig_client_order_id: Optional[str] = None
    ) -> JsonObject:
        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.query_oco_order,
            signed=True,
            params={
                "orderListId": order_list_id,
                "origClientOrderId": orig_client_order_id
            }
        )
    
    async def query_all_oco_order(
        self,
        from_id: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: Optional[int] = None
    ) -> JsonObject:
        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.query_all_oco_order,
            signed=True,
            params={
                "fromId": from_id,
                "startTime": start_time,
                "endTime": end_time,
                "limit": limit
            }
        )
    
    async def query_open_oco_order(self) -> JsonObject:
        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.query_open_oco_order,
            signed=True
        )
    
    async def account_info(self) -> JsonObject:
        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.account_info,
            signed=True
        )
    
    async def account_trade_list(
        self,
        symbol: str,
        order_id: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        from_id: Optional[int] = None,
        limit: Optional[int] = None
    ) -> JsonObject:
        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.account_trade_list,
            signed=True,
            params={
                "symbol": symbol,
                "orderId": order_id,
                "startTime": start_time,
                "endTime": end_time,
                "fromId": from_id,
                "limit": limit
            }
        )
    
    async def order_rate_limit(self) -> JsonObject:
        return await self._client.request(
            method="GET",
            url=self._client._API_URL + self._client._endpoints.order_rate_limit,
            signed=True
        )
