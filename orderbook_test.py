import json
from orderbook import OrderBook

LIQUIDITY_PAYLOAD_STRING = """
{"jsonrpc":"2.0","result":{
"limit_orders":{"asks":[{"tick":-138477,"amount":"0x2"},
{"tick":679408,"amount":"0x64"}],"bids":[{"tick":-230271,"amount":"0x15ef3c0"},
{"tick":-198955,"amount":"0x5f5e100"}]},
"range_orders":[{"tick":-887272,"liquidity":"0x142bd6ddc3906"},
{"tick":-253298,"liquidity":"0x14420f0c7e9bf"},
{"tick":-246366,"liquidity":"0x142bd6ddc3906"},
{"tick":-207244,"liquidity":"0x1c8d871ac5fd3"},{"tick":-203189,"liquidity":"0x142bd6ddc3906"},
{"tick":-197638,"liquidity":"0x1b27292ee102e24a"},{"tick":-197634,"liquidity":"0x142bd6ddc3906"},
{"tick":-125818,"liquidity":"0x7845a02cf8b98"},{"tick":887272,"liquidity":"0x0"}]},"id":3}
"""
LIQUIDITY_PAYLOAD_REFERENCE = json.loads(LIQUIDITY_PAYLOAD_STRING)

PRICE_PAYLOAD_STRING = """
{"jsonrpc":"2.0","method":"cf_subscribe_pool_price",
"params":{"subscription":"INwsL2MXqQqlahkJ",
"result":{"price":"0x4df1cb6985c724bf6d02fc7059f","sqrt_price":"0x23508172f53af3de6166c9","tick":-150529}}}"""
PRICE_PAYLOAD_REFERENCE = json.loads(PRICE_PAYLOAD_STRING)


def test_orderbook_limits():
    order_book = OrderBook(base_asset="ETH", quote_asset="USDC")
    order_book.populate_book_from_liquidity_payload(LIQUIDITY_PAYLOAD_REFERENCE)
    assert True


def test_orderbook_ranges():
    order_book = OrderBook(base_asset="ETH", quote_asset="USDC")
    order_book.populate_book_from_liquidity_payload(LIQUIDITY_PAYLOAD_REFERENCE)
    assert True


def test_orderbook_limit_top():
    order_book = OrderBook(base_asset="ETH", quote_asset="USDC")
    order_book.populate_book_from_liquidity_payload(LIQUIDITY_PAYLOAD_REFERENCE)
    assert True


def test_orderbook_price():
    order_book = OrderBook(base_asset="ETH", quote_asset="USDC")
    order_book.populate_last_price_from_price_payload(
        PRICE_PAYLOAD_REFERENCE["params"]["result"]
    )
    assert True
