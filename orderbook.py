import json
import math
import logging
from typing import List

"""
Amount
An integer encoded as a big-endian hex string, between 0 and 2^128 - 1, 
representing a quantity of a token in it's smallest unit.
For example, ETH uses 18 decimal places, so 100ETH is 100,000,000,000,000,000,000 Units, 
which encoded as hex is "0x56bc75e2d63100000". 
As another example, USDC uses 6 decimals, so 10USDC is 10,000,000 Units, which encoded as hex is "0x989680".

Liquidity
An integer encoded as a big-endian hex string, between 0 and 2^128 - 1, 
representing the amount of liquidity in/the size of a range order.

Ticks
An integer between -887272 and 887272 inclusively representing a price. 
To calculate the nearest tick to a given price in the quote asset, 
use this formula: 
log1.0001(price * <QUOTE_ASSET_PRECISION> / <BASE_ASSET_PRECISION>). 
The tick representation of a price can be calculated by taking the log1.0001 of the price in the quote asset, 
and rounded down to the nearest integer. 
A tick can be turned into a price (into the quote asset) with this formula: 
(1.0001^tick) * <BASE_ASSET_PRECISION> / <QUOTE_ASSET_PRECISION>. 
<ASSET_PRECISION> for ETH would be 10^18 and for USDC it would be 10^6.

Price
A 256 bit unsigned fixed point number, with 128 fractional bits, 
representing a price as the amount of quote asset a single unit of the base asset is valued at. 
Note the amounts are in the smallest units of both assets.

For example the price 10000 USDC/ETH represented in this format would be:
floor_to_integer((10000 * 10^6 / 10^18) * 2^128) = 3402823669209384634633746074317. 
Note the 10^6 is 1 USDC is USDC's smallest unit, 10^18 is 1 ETH in ETH's smallest unit (wei), 
and the 128 in 2^128 in the number of fractional bits in the price, which as stated above is 128.
"""

ASSETS_PRECISION = {"ETH": 10**18, "USDC": 10**6}


def hex_to_decimal(hex_string: str):
    return int(hex_string, 16)


def tick_to_price(
    tick: int, base_asset_precision: int, quote_asset_precision: int
) -> float:
    return 1.0001**tick * (base_asset_precision / quote_asset_precision)


def price_to_tick(
    price: float, base_asset_precision: int, quote_asset_precision: int
) -> int:
    return math.log(price * quote_asset_precision / base_asset_precision, 1.0001)


def price_to_market_price(
    price: int, base_asset_precision: int, quote_asset_precision: int
):
    market_price = (price / 2**128) * (base_asset_precision / quote_asset_precision)
    return market_price


class OrderBook:

    def __init__(self, base_asset: str, quote_asset: str):
        self.base_asset = base_asset
        self.quote_asset = quote_asset
        self.limit_price_points = {"asks": {}, "bids": {}}
        self.range_price_points = []
        self.bid_max_tick = -887272  # initialization value as min possible
        self.ask_min_tick = 887272  # initialization value as max possible

    def populate_from_liquidity_payload(self, liquidity_payload: dict) -> None:
        """
        Taking the whole liquidity payload from cf_pool_liquidity
        and repopulating the data structures
        There is no real way to subscribe/query diffs or single order feeds
        or to save real orders with priority, for the same tick for example
        """
        self.limit_price_points = {"asks": {}, "bids": {}}
        self.range_price_points = []
        self.range_price_points = liquidity_payload["result"]["range_orders"]
        try:
            for order in liquidity_payload["result"]["limit_orders"]["asks"]:
                self.limit_price_points["asks"][order["tick"]] = order["amount"]
        except KeyError:
            logging.info("missing limit asks in liquidity returned payload")
        try:
            for order in liquidity_payload["result"]["limit_orders"]["bids"]:
                self.limit_price_points["bids"][order["tick"]] = order["amount"]
        except KeyError:
            logging.info("missing limit bids in liquidity returned payload")

    # the below two methods I am not quite sure who they could be implemented
    # as they assume and id lookup and implicitly the account as well if I understand correctly
    def add_range_order(self, id: int, tick_range: List[int], size: int):
        """
        - base_asset
        - quote_asset
        - id
        - tick_range (Optional): A JSON array of two Ticks,
        representing the lower and upper bound of the order's price range.
          Must be specified if no range order with the specified id exists in this pool.
          If not specified, the tick range of the existing order with the same id will be used.
        - size
        - wait_for
        """
        pass

    def add_limit_order(self, id: int, side: str, sell_amont: int, tick: int = None):
        """
        - side:
        - id:
        - tick:  (Optional): The price of the limit order.
        - sell_amount: The amount of assets the limit order should sell. For "buy" orders,
        this is measured in the quote asset,
        and for "sell" orders, this is measured in the base asset.
        """
        pass

    def __str__(self) -> str:
        """
        Book string representation for logging/visulization
        """
        return "".join(
            [
                "Book range price points: ",
                str(self.range_price_points),
                "\n",
                "Book limit orders: ",
                str(self.limit_price_points),
            ]
        )
