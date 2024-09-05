import unittest
from src.model import DynamicFeeModel
import numpy as np

class TestDynamicFeeModel(unittest.TestCase):
    def setUp(self):
        self.model = DynamicFeeModel()

    def test_update_and_predict(self):
        sample_data = {
            'price': 1000, 
            'volume': 500000, 
            'liquidity': 1000000, 
            'volatility': 0.05, 
            'current_fee': 0.003
        }
        new_fee = self.model.update_and_predict(sample_data)
        self.assertIsInstance(new_fee, float)
        self.assertTrue(0.0005 <= new_fee <= 0.01)  # Fee should be between 0.05% and 1%

    def test_fee_bounds(self):
        # Test lower bound
        self.model.data = [{'price': 1000, 'volume': 500000, 'liquidity': 1000000, 'volatility': 0.01, 'current_fee': 0.0001}] * 100
        new_fee = self.model.update_and_predict(self.model.data[-1])
        self.assertGreaterEqual(new_fee, 0.0005)

        # Test upper bound
        self.model.data = [{'price': 1000, 'volume': 500000, 'liquidity': 1000000, 'volatility': 0.5, 'current_fee': 0.02}] * 100
        new_fee = self.model.update_and_predict(self.model.data[-1])
        self.assertLessEqual(new_fee, 0.01)

if __name__ == '__main__':
    unittest.main()