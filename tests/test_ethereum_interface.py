import unittest
from unittest.mock import patch, MagicMock
from src.ethereum_interface import EthereumInterface
from src.config import load_config

class TestEthereumInterface(unittest.TestCase):
    def setUp(self):
        self.config = load_config()
        self.interface = EthereumInterface(self.config)

    @patch('web3.Web3')
    def test_connect(self, mock_web3):
        mock_web3.WebsocketProvider.return_value = MagicMock()
        mock_web3.is_connected.return_value = True
        self.interface.connect()
        self.assertIsNotNone(self.interface.w3)
        self.assertIsNotNone(self.interface.oracle_contract)
        self.assertIsNotNone(self.interface.pool_contract)

    @patch('web3.Web3')
    def test_update_fee(self, mock_web3):
        mock_web3.WebsocketProvider.return_value = MagicMock()
        mock_web3.is_connected.return_value = True
        self.interface.connect()
        
        mock_tx_hash = '0x1234'
        mock_receipt = MagicMock()
        mock_receipt.transactionHash.hex.return_value = mock_tx_hash
        
        self.interface.w3.eth.send_raw_transaction = MagicMock(return_value=mock_tx_hash)
        self.interface.w3.eth.wait_for_transaction_receipt = MagicMock(return_value=mock_receipt)
        
        new_fee = 0.005
        self.interface.update_fee(new_fee)
        
        self.interface.w3.eth.send_raw_transaction.assert_called_once()
        self.interface.w3.eth.wait_for_transaction_receipt.assert_called_once_with(mock_tx_hash)

    # Add more tests as needed