# JIT Strategies Tech Challenge

Creating a subscription framework and OrderBook as detailed in "Developer_Test_JIT_chainflip.pdf"

## To run locally

- `git clone` the repo locally
- follow the instructions here for node spin up: https://github.com/chainflip-io/chainflip-perseverance
- create venv out of requirements.txt
- `python framework.py` for default ETH to USDC or
- `python framework.py --base_asset=<your asset> --quote_asset=<your asset>`

## Run Tests

- `pytest` on the base folder will run all the orderbook tests

## Things I wasn't sure about:

- Price representation:
  - I tried
  - I tried
    still doesn't make sense to me
- cf_subscribe_prewitness_swaps doesn't really return any inbound message even if left run for a while
