from web3 import Web3
import json
import dotenv as _dotenv
import os as os
import pandas as pd
_dotenv.load_dotenv()

infura_url = os.environ["POLYGON"]
web3 = Web3(Web3.HTTPProvider(infura_url))

# V3 Pool Address
contract_address = '0xEFa98Fdf168f372E5e9e9b910FcDfd65856f3986'

with open('./utils/v3-pools.json', 'r') as f:
  abi_pools = json.load(f)

contract = web3.eth.contract(address=contract_address, abi=abi_pools)

# Ranges for the loop
start_index = 0
end_index = web3.eth.blockNumber
increment = 2500

pools_data = []
# Loop
for i in range(start_index, end_index, increment):
    print(i)

    event = contract.events.Swap().getLogs(fromBlock=i, toBlock=i+increment)

    for event in event:
        recipient = event['args']['recipient']
        amount0 = event['args']['amount0']
        amount1 = event['args']['amount1']
        sqrtPriceLimitX96 = event['args']['sqrtPriceX96']
        liquidity = event['args']['liquidity']
        tick = event['args']['tick']
        event_type = event['event']
        logIndex = event['logIndex']
        transactionIndex = event['transactionIndex']
        tx_hash = event['transactionHash'].hex()
        block_number = event['blockNumber']

        pool_data = {
            'Recipient': recipient,
            'Amount 0': amount0,
            'Amount 1': amount1,
            'Sqrt': sqrtPriceLimitX96,
            'Liquidity': liquidity,
            'Tick': tick,
            'Event': event_type,
            'LogIndex': logIndex,
            'TransactionIndex': transactionIndex,
            'Tx Hash': tx_hash,
            'BlockNumber': block_number
        }

        pools_data.append(pool_data)

        print("New Swap event recorded:")
        print()
        print("Recipient:", recipient)
        print("Amount 0:", amount0)
        print("Amount 1:", amount1)
        print("Sqrt Price Limit X96:", sqrtPriceLimitX96)
        print("Liquidity:", liquidity)
        print("Tick:", tick)
        print("Event:", event_type)
        print("Log Index:", logIndex)
        print("Transaction Index:", transactionIndex)
        print("Tx Hash:", tx_hash)
        print("Block Number:", block_number)
        print()
        print("----------------------------------------------------")

# Create a DataFrame from the swap events data
df = pd.DataFrame(pools_data)

# Save the DataFrame to a CSV file
csv_filename = 'events_swap.csv'
df.to_csv(csv_filename, index=False)