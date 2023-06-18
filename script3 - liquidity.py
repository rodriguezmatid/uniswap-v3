from web3 import Web3
import json
import dotenv as _dotenv
import os as os
import pandas as pd

_dotenv.load_dotenv()                       # Loading the environment variables from the .env file

infura_url = os.environ["POLYGON"]          # Fetching the Infura URL from the environment variables
web3 = Web3(Web3.HTTPProvider(infura_url))  # Creating a Web3 instance with the Infura URL

# Uniswap V3 Pool contract address
contract_address = web3.toChecksumAddress('0xEFa98Fdf168f372E5e9e9b910FcDfd65856f3986')

with open('./utils/v3-pools.json', 'r') as f:
  abi_pools = json.load(f)                  # Loading the contract ABI from the JSON file

with open('./utils/erc20-v3.json', 'r') as f:
  abi_erc20 = json.load(f)                  # Loading the ERC20 contract ABI from the JSON file

contract = web3.eth.contract(address=contract_address, abi=abi_pools)
token_0 = contract.functions.token0().call()
token_1 = contract.functions.token1().call()
token_0_contract = web3.eth.contract(address=token_0, abi=abi_erc20)
token_1_contract = web3.eth.contract(address=token_1, abi=abi_erc20)
token_0_decimals = token_0_contract.functions.decimals().call()
token_1_decimals = token_1_contract.functions.decimals().call()

print("Token 0: ", token_0)
print("Token 1: ", token_1)
print("Token 0 Decimals: ", token_0_decimals)
print("Token 1 Decimals: ", token_1_decimals)
print()

amounts0 = 0
amounts1 = 0
liquidity = 0
tick_spacing = contract.functions.tickSpacing().call()
slot0 = contract.functions.slot0().call()
actual_tick = slot0[1]
actual_price = 1/((1.0001 ** actual_tick) / (10**token_1_decimals))/ (10**token_0_decimals) # price of 1 token 0 in terms of token 1
intermidiate_price = 1/(((slot0[0]/(2**96)) ** 2) / (10**token_1_decimals))/ (10**token_0_decimals)
sqrtPriceCurrent = slot0[0] / (1<<96)

print("Actual Tick: ", actual_tick)
print("Actual Price: ", actual_price)
print("Actual Intermidiate Price: ", intermidiate_price)

def calculate_token0_amount(liquidity, sqrtPriceCurrent, sqrtPriceLow, sqrtPriceHigh):
    sqrtPriceCurrent = max(min(sqrtPriceCurrent, sqrtPriceHigh), sqrtPriceLow)
    return liquidity * (sqrtPriceHigh - sqrtPriceCurrent) / (sqrtPriceCurrent * sqrtPriceHigh)

def calculate_token1_amount(liquidity, sqrtPriceCurrent, sqrtPriceLow, sqrtPriceHigh):
    sqrtPriceCurrent = max(min(sqrtPriceCurrent, sqrtPriceHigh), sqrtPriceLow)
    return liquidity * (sqrtPriceCurrent - sqrtPriceLow)

MIN_TICK = 201710 
MAX_TICK = 201790
counter = 0
data = []                                  # List to store the data

for tick in range(MIN_TICK, MAX_TICK, tick_spacing):
  
  mi_tick = tick
  ticks_information = contract.functions.ticks(tick).call()
  liquidity_gross = ticks_information[0]
  liquidity_net = ticks_information[1]
  feeGrowthOutside0X128 = ticks_information[2]
  feeGrowthOutside1X128 = ticks_information[3]
  tickCumulativeOutside = ticks_information[4]
  secondsPerLiquidityOutsideX128 = ticks_information[5]
  secondsOutside = ticks_information[6]
  initialized = ticks_information[7]
  
  sqrtPriceLow = 1.0001 ** (tick // 2)
  sqrtPriceHigh = 1.0001 ** ((tick + tick_spacing) // 2)
  print(sqrtPriceCurrent)
  print(sqrtPriceLow)
  print(sqrtPriceHigh)
  amounts0 = calculate_token0_amount(liquidity_net, sqrtPriceCurrent, sqrtPriceLow, sqrtPriceHigh)
  amounts1 = calculate_token1_amount(liquidity_net, sqrtPriceCurrent, sqrtPriceLow, sqrtPriceHigh)

  word_pos = mi_tick // (2** 8)
  bit_pos = mi_tick % 256

  counter = counter + 1
  print("Counter: ", counter)
  print(f"Word {word_pos}, bit {bit_pos}")

  print("Tick: ", mi_tick)
  print("Liquidity Net: ", liquidity_net)
  print("Liquidity Gross: ", liquidity_gross)
  print("Liquidity feeGrowthOutside0X128: ", feeGrowthOutside0X128)
  print("Liquidity feeGrowthOutside1X128: ", feeGrowthOutside1X128)
  print("Liquidity tickCumulativeOutside: ", tickCumulativeOutside)
  print("Liquidity secondsPerLiquidityOutsideX128: ", secondsPerLiquidityOutsideX128)
  print("Liquidity secondsOutside: ", secondsOutside)
  print("Liquidity initialized: ", initialized)
  print(amounts0)
  print(amounts1)
  print()
  print("----------------------------------------------------")

  # Add the values to the data list
  data.append({
      'Amounts0': amounts0,
      'Amounts1': amounts1
  })

print("Amount 0: ", amounts0) 
print("Amount 1: ", amounts1)