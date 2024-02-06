# JIT Strategies Tech Challenge

Creating a subscription framework and OrderBook as detailed in "Developer_Test_JIT_chainflip.pdf"

## To run locally

- `git clone` the repo locally
- follow the instructions here for node spin up: https://github.com/chainflip-io/chainflip-perseverance
- create venv (I used python 3.10.12) and install requirements.txt
- run `python framework.py` for default ETH to USDC or
- run `python framework.py --base_asset=<your asset> --quote_asset=<your asset>`
  if the pool does not exist it will raise a KeyError from one of the error messages returned,
  but from the logs should be clear that the reason is the missing pool for that combination.
  Maybe writing better error handling for the future.

## Run Tests

- `pytest` on the base folder will run all the orderbook.py tests

## Things I wasn't sure about:

- Price representation:
  as an example from a price update message from ETH/USDC

  - I tried from the tick using the functions in order book:

    - `In [23]: tick_to_price(-153861, ASSETS_PRECISION['ETH'], ASSETS_PRECISION['USDC'])`
    - `Out[23]: 208082.59467484668`

  - I tried from the price representation:

    - `In [28]: price_returned = int("0x37db83b756d0a7932f35b7479ed", 16)`
    - `In [29]: price_to_market_price(price_returned, ASSETS_PRECISION['ETH'], ASSETS_PRECISION['USDC'])`
    - `Out[29]: 208085.32304775115`

    the 2 seems consistent but I still don't quite understand how to get the 2360.19 ETH/USDC
    standard price representation of today as I am writing.

    I think the OrderBook logic should still work on the generalized tick model when inserting orders.

- cf_subscribe_prewitness_swaps doesn't really return any inbound message even if left run for a while
  maybe this is expected on the perseverance chain but then I am not sure how those few price change messages
  end up being generated.
