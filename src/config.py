import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    
    config = {
        'ETHEREUM': {
            'WSS_ENDPOINT': os.getenv('ETHEREUM_WSS_ENDPOINT'),
            'PRIVATE_KEY': os.getenv('ETHEREUM_PRIVATE_KEY'),
            'POLL_INTERVAL': os.getenv('POLL_INTERVAL', '2')
        },
        'CONTRACT': {
            'ORACLE_ADDRESS': os.getenv('ORACLE_CONTRACT_ADDRESS'),
            'POOL_ADDRESS': os.getenv('POOL_CONTRACT_ADDRESS'),
            'ORACLE_ABI_PATH': os.getenv('ORACLE_ABI_PATH', 'abis/oracle_abi.json'),
            'POOL_ABI_PATH': os.getenv('POOL_ABI_PATH', 'abis/pool_abi.json')
        },
        'MODEL': {
            'FILE_PATH': os.getenv('MODEL_FILE_PATH', 'model_state.joblib')
        },
        'LOGGING': {
            'LEVEL': os.getenv('LOG_LEVEL', 'INFO')
        }
    }
    
    return config