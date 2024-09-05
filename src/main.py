import asyncio
import logging
from src.ethereum_interface import EthereumInterface
from src.data_processor import DataProcessor
from src.model import DynamicFeeModel
from src.config import load_config
from src.utils import setup_logging

async def main():
    config = load_config()
    setup_logging(config['LOGGING']['LEVEL'])
    
    eth_interface = EthereumInterface(config)
    data_processor = DataProcessor()
    model = DynamicFeeModel.load_or_initialize(config['MODEL']['FILE_PATH'])

    await eth_interface.connect()

    async for event_data in eth_interface.listen_for_events():
        try:
            processed_data = data_processor.process(event_data)
            new_fee = model.update_and_predict(processed_data)
            if data_processor.is_change_significant(new_fee, model.current_fee):
                await eth_interface.update_fee(new_fee)
                model.current_fee = new_fee
            
            model.save(config['MODEL']['FILE_PATH'])
        except Exception as e:
            logging.error(f"Error processing event: {e}")

if __name__ == "__main__":
    asyncio.run(main())