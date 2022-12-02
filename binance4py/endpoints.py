from dataclasses import dataclass


@dataclass
class Endpoints:
    # General endpoints
    ping: str = "v3/ping"
    server_time: str = "v3/time"
    exchange_info: str = "v3/exchangeInfo"
    # Market Data endpoints
    order_book: str = "v3/depth"
    recent_trades: str = "v3/trades"
    old_trades: str = "v3/historicalTrades"
    aggregate_trades: str = "v3/aggTrades"
    klines: str = "v3/klines"
    ui_klines: str = "v3/uiKlines"
    average_price: str = "v3/avgPrice"
    ticker_24hr: str = "v3/ticker/24hr"
    price_ticker: str = "v3/ticker/price"
    order_book_ticker: str = "v3/ticker/bookTicker"
    rolling_window_ticker: str = "v3/ticker"
    # Spot Account/Trade endpoints
    create_test_order: str = "v3/order/test"
    create_order: str = "v3/order"
    cancel_order: str = "v3/order"
    cancel_all_open_orders: str = "v3/openOrders"
    query_order: str = "v3/order"
    replace_order: str = "v3/order/cancelReplace"
    open_orders: str = "v3/openOrders"
    all_orders: str = "v3/allOrders"
    create_oco_order: str = "v3/order/oco"
    cancel_oco_order: str = "v3/orderList"
    query_oco_order: str = "v3/orderList"
    query_all_oco_order: str = "v3/allOrderList"
    query_open_oco_order: str = "v3/openOrderList"
    account_info: str = "v3/account"
    account_trade_list: str = "v3/myTrades"
    order_rate_limit: str = "v3/rateLimit/order"
    # Websocket
    create_listen_key: str = "v3/userDataStream"
    keep_alive_listen_key: str = "v3/userDataStream"
    close_listen_key: str = "v3/userDataStream"
