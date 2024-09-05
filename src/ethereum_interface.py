from web3 import Web3
import asyncio
import json
import logging

logger = logging.getLogger(__name__)

class EthereumInterface:
    def __init__(self, config):
        self.config = config
        self.w3 = None
        self.oracle_contract = None
        self.pool_contract = None

    async def connect(self):
        self.w3 = Web3(Web3.WebsocketProvider(self.config['ETHEREUM']['WSS_ENDPOINT']))
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to Ethereum node")
        
        with open(self.config['CONTRACT']['ORACLE_ABI_PATH']) as f:
            oracle_abi = json.load(f)
        
        with open(self.config['CONTRACT']['POOL_ABI_PATH']) as f:
            pool_abi = json.load(f)
        
        self.oracle_contract = self.w3.eth.contract(
            address=self.config['CONTRACT']['ORACLE_ADDRESS'],
            abi=oracle_abi
        )
        
        self.pool_contract = self.w3.eth.contract(
            address=self.config['CONTRACT']['POOL_ADDRESS'],
            abi=pool_abi
        )

    async def get_latest_swap_event(self):
        event_filter = self.pool_contract.events.Swap.create_filter(fromBlock='latest')
        events = event_filter.get_new_entries()
        if events:
            return events[-1]['args']
        else:
            raise ValueError("No swap events found")

    async def get_recent_swap_events(self, number_of_events):
        current_block = self.w3.eth.block_number
        event_filter = self.pool_contract.events.Swap.create_filter(fromBlock=current_block - 1000)  # Assume 1000 blocks is enough
        events = event_filter.get_all_entries()
        return [event['args'] for event in events[-number_of_events:]]

    async def get_current_fee(self):
        return self.pool_contract.functions.fee().call() / 1000000  # Convert from uint24 to decimal


    async def listen_for_events(self):
        event_filter = self.pool_contract.events.Swap.create_filter(fromBlock='latest')
        while True:
            for event in event_filter.get_new_entries():
                yield event['args']
            await asyncio.sleep(float(self.config['ETHEREUM']['POLL_INTERVAL']))

    async def update_fee(self, new_fee):
        account = self.w3.eth.account.from_key(self.config['ETHEREUM']['PRIVATE_KEY'])
        nonce = self.w3.eth.get_transaction_count(account.address)
        
        fee_in_basis_points = int(new_fee * 10000)
        
        txn = self.oracle_contract.functions.updateFee(fee_in_basis_points).build_transaction({
            'from': account.address,
            'nonce': nonce,
            'gas': 200000,  # Adjust as needed
            'gasPrice': self.w3.eth.gas_price
        })
        signed_txn = account.sign_transaction(txn)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        logger.info(f"Fee updated to {new_fee}. Transaction hash: {receipt.transactionHash.hex()}")