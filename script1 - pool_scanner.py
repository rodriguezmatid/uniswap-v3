# Importing libraries
from web3 import Web3
import json
import dotenv as _dotenv
import os as os
import pandas as pd

_dotenv.load_dotenv() # Loading the environment variables from the .env file

infura_url = os.environ["POLYGON"] # Fetching the Infura URL from the environment variables
web3 = Web3(Web3.HTTPProvider(infura_url)) # Creating a Web3 instance with the Infura URL

# Uniswap V3 Factory Address
contract_address = '0x1F98431c8aD98523631AE4a59f267346ea31F984'

event_name = 'PoolCreated'

with open('./utils/v3-factory.json', 'r') as f: # Loading the contract ABI from the JSON file
  abi_factory = json.load(f)

# Getting the Factory contract
contract = web3.eth.contract(address=contract_address, abi=abi_factory)

# Loop ranges
start_index = 0
end_index = web3.eth.blockNumber
increment = 2500
pools_data = [] # List to store pool data

# Loop
for i in range(start_index, end_index, increment):
    print(i)

    events = contract.events.PoolCreated().getLogs(fromBlock=i, toBlock=i+increment)
    for event in events:

        token0 = event['args']['token0']
        token1 = event['args']['token1']
        fee = event['args']['fee']
        tick_spacing = event['args']['tickSpacing']
        pool = event['args']['pool']
        tx_hash = event['transactionHash'].hex()
        block_number = event['blockNumber']

        pool_data = {
            'Token 0': token0,
            'Token 1': token1,
            'Fee': fee,
            'tickSpacing': tick_spacing,
            'Pool': pool,
            'Tx Hash': tx_hash,
            'BlockNumber': block_number
        }

        pools_data.append(pool_data) # Appending pool data to the list

        print("New pool created:")
        print()
        print("Token 0:", token0)
        print("Token 1:", token1)
        print("Fee:", fee)
        print("tickSpacing:", tick_spacing)
        print("Pool:", pool)
        print("Tx Hash:", tx_hash)
        print("BlockNumber:", block_number)
        print()
        print("----------------------------------------------------")

# Creating a DataFrame from the pool data
df = pd.DataFrame(pools_data)

# Saving the DataFrame to a CSV file
csv_filename = 'script1_results.csv'
df.to_csv(csv_filename, index=False)