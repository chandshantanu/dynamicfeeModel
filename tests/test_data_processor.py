import unittest
from src.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DataProcessor()

    def test_process(self):
        event_data = {'price': '1000', 'volume': '500000', 'liquidity': '1000000', 'current_fee': '0.003'}
        processed_data = self.processor.process(event_data)
        self.assertIn('volatility', processed_data)
        self.assertIsInstance(processed_data['volatility'], float)
        self.assertGreaterEqual(processed_data['volatility'], 0)

    def test_is_change_significant(self):
        self.assertTrue(self.processor.is_change_significant(0.0031, 0.003, threshold=0.0001))
        self.assertFalse(self.processor.is_change_significant(0.00301, 0.003, threshold=0.0001))

if __name__ == '__main__':
    unittest.main()