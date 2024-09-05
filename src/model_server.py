from flask import Flask, jsonify
from .model import DynamicFeeModel
from .data_processor import DataProcessor
from .config import load_config
from .ethereum_interface import EthereumInterface
import asyncio

app = Flask(__name__)

config = load_config()
model = DynamicFeeModel.load_or_initialize(config['MODEL']['FILE_PATH'])
data_processor = DataProcessor()
eth_interface = EthereumInterface(config)

def initialize_eth_interface():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(eth_interface.connect())

# Initialize Ethereum interface before first request
initialize_eth_interface()

async def get_latest_market_data():
    # Fetch the latest swap event from the Uniswap V3 pool
    latest_swap = await eth_interface.get_latest_swap_event()
    
    # Extract relevant data from the swap event
    price = calculate_price(latest_swap['sqrtPriceX96'])
    volume = abs(latest_swap['amount0']) + abs(latest_swap['amount1'])
    liquidity = latest_swap['liquidity']
    
    # Get the current fee from the pool contract
    current_fee = await eth_interface.get_current_fee()
    
    # Calculate volatility (this is a simplified version)
    volatility = await calculate_volatility()
    
    return {
        'price': price,
        'volume': volume,
        'liquidity': liquidity,
        'current_fee': current_fee,
        'volatility': volatility
    }

def calculate_price(sqrtPriceX96):
    # Convert sqrtPriceX96 to actual price
    price = (sqrtPriceX96 / (2**96)) ** 2
    return price

async def calculate_volatility():
    # Fetch recent swap events
    recent_swaps = await eth_interface.get_recent_swap_events(100)  # Last 100 swaps
    prices = [calculate_price(swap['sqrtPriceX96']) for swap in recent_swaps]
    
    # Calculate standard deviation of prices
    mean_price = sum(prices) / len(prices)
    variance = sum((price - mean_price) ** 2 for price in prices) / len(prices)
    return (variance ** 0.5) / mean_price  # Coefficient of variation as volatility

@app.route('/get_fee', methods=['GET'])
async def get_fee():
    # Get latest market data
    event_data = await get_latest_market_data()
    
    # Process the data
    processed_data = data_processor.process(event_data)
    
    # Use the model to predict the fee
    new_fee = model.update_and_predict(processed_data)
    
    # Convert to basis points (e.g., 0.003 becomes 3000)
    fee_basis_points = int(new_fee * 10000)
    
    return jsonify({"fee": fee_basis_points})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)