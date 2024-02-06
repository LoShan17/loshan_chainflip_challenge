import asyncio
import aiohttp
import json
import logging
from orderbook import OrderBook

logging.basicConfig(
    encoding="utf-8",
    level=logging.DEBUG,
    filename="chainflip_framework.log",
    format="%(asctime)s %(message)s",
)

from jsonrpcclient import request_json, request
import websockets


HTTP_URL = "http://localhost:9944"
WS_URL = "ws://localhost:9944"


# prewitnessed swaps subscription string json
# {"jsonrpc":"2.0","id":"1","method":"cf_subscribe_prewitness_swaps","params":["Btc", "Eth"]}
# docs seem wrong on params, whereas with the "from_asset" .... "to_asset" faomatting the calls returns
json_str_payload_prewitness_swaps_subscription = request_json(
    "cf_subscribe_prewitness_swaps", params={"from_asset": "ETH", "to_asset": "USDC"}
)

# pool price subscription string json
json_str_payload_pool_price_subscription = request_json(
    "cf_subscribe_pool_price", params={"from_asset": "ETH", "to_asset": "USDC"}
)

# examples of parsing responses
# example_message_price = '{"jsonrpc":"2.0","method":"cf_subscribe_pool_price","params":{"subscription":"WyWzpPPkLIV8NErb","result":{"price":"0x393d4b7e97617d02dd59df31a5a9","sqrt_price":"0x790d00e1da61e22eda2ba9","tick":-125890}}}'
# example_message_liquidity = "{'jsonrpc': '2.0', 'result': {'limit_orders': {'asks': [{'tick': 679408, 'amount': '0x64'}], 'bids': [{'tick': -230271, 'amount': '0x15ef3c0'}, {'tick': -199320, 'amount': '0x5f5e100'}]}, 'range_orders': [{'tick': -887272, 'liquidity': '0x142bd6ddc3906'}, {'tick': -253298, 'liquidity': '0x14420f0c7e9bf'}, {'tick': -246366, 'liquidity': '0x142bd6ddc3906'}, {'tick': -207244, 'liquidity': '0x1c8d871ac5fd3'}, {'tick': -203189, 'liquidity': '0x142bd6ddc3906'}, {'tick': -197638, 'liquidity': '0x1b27292ee102e24a'}, {'tick': -197634, 'liquidity': '0x142bd6ddc3906'}, {'tick': -125818, 'liquidity': '0x7845a02cf8b98'}, {'tick': 887272, 'liquidity': '0x0'}]}, 'id': 1}"
# example_message_liquidity = example_message_liquidity.replace("'", '"')

# price_message_dictionary = json.loads(example_message_price)
# liquidity_message_dictionary = json.loads(example_message_liquidity)


# again "params" definition doesn't seem to be correct in the docs
# (pair_asset instead of quote_asset)
async def query_pool_liquidity(
    params: dict = {"base_asset": "ETH", "quote_asset": "USDC"}
) -> dict:
    """
    Returns full dictionary as payload as described in the docs like:
    {"jsonrpc": "2.0","result": {
        "limit_orders": { "base": [], "pair": [] },
        "range_orders": [[-887272, 3161961432402363],[887272, 0]]
      },
      "id": 1
    }
    """
    async with aiohttp.ClientSession() as session:
        payload_liquidity_call = request("cf_pool_liquidity", params=params)
        logging.info(payload_liquidity_call)
        async with session.post(HTTP_URL, json=payload_liquidity_call) as response:
            logging.info(response.status)
            logging.info(await response.text())
            return json.loads(await response.text())


async def main():
    """
    main subscription loop. The only 2 things that can be subscribed are prewitness_swaps and pool_price
    I can then query explicitly the liquidity pool when there is an update in either of them
    """
    order_book = OrderBook(base_asset="ETH", quote_asset="USDC")
    async with websockets.connect(WS_URL) as ws:
        logging.info("Inside the main subscription loop")
        await ws.send(json_str_payload_pool_price_subscription)
        logging.info("sent pool price subscription")
        await ws.send(json_str_payload_prewitness_swaps_subscription)
        logging.info("sent prewitness swap subscription")
        async for message in ws:
            logging.info(message)
            message_dictionary = json.loads(message)
            # if this message is a subscription response to either subscriptions
            # will make a call to cf_pool_liquidity either on price change or on prewitness_swap deposit
            if "method" in message_dictionary:
                liquidity_dictionary = await query_pool_liquidity()
                logging.info(liquidity_dictionary)
                order_book.populate_from_liquidity_payload(
                    liquidity_payload=liquidity_dictionary
                )
                logging.info(str(order_book))


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        logging.info("Keyboard exit received, exiting")
