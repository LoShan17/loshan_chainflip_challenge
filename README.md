# JIT Strategies Tech Challenge

Creating a subscription framework and OrderBook as detailed in "Developer_Test_JIT_chainflip.pdf"

## To run locally

- `git clone` the repo locally
- follow the instructions here for node spin up: https://github.com/chainflip-io/chainflip-perseverance
- create venv (I used python 3.10.12) and install requirements.txt
- run `python framework.py` for default ETH to USDC or
- run `python framework.py --base_asset=<your asset> --quote_asset=<your asset>`
  if the pool does not exist it will raise a KeyError from one of the error messages returned,
  but from the logs should be clear that is the reason is the missing pool for that combination.
  Maybe writing better error handling for the future.

## Run Tests

- `pytest` on the base folder will run all the orderbook.py tests

## Things I wasn't sure about:

- Price representation:
  as an example
  - I tried
  - I tried
    I think the OrderBook logic should still work on the generalized tick model of the exchange
    but the final representtaion still doesn't make sense to me.
- cf_subscribe_prewitness_swaps doesn't really return any inbound message even if left run for a while
  maybe this is expected on the perseverance chain but then I am not sure those few price change messages how are they generated.
