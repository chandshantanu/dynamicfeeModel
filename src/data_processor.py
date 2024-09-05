import numpy as np

class DataProcessor:
    def __init__(self):
        self.price_history = []

    def process(self, event_data):
        price = float(event_data['price'])
        volume = float(event_data['volume'])
        liquidity = float(event_data['liquidity'])
        current_fee = float(event_data['current_fee'])

        self.price_history.append(price)
        if len(self.price_history) > 100:
            self.price_history = self.price_history[-100:]

        volatility = self.calculate_volatility()

        return {
            'price': price,
            'volume': volume,
            'liquidity': liquidity,
            'volatility': volatility,
            'current_fee': current_fee
        }

    def calculate_volatility(self, window=20):
        if len(self.price_history) < 2:
            return 0
        returns = np.log(np.array(self.price_history[1:]) / np.array(self.price_history[:-1]))
        return np.std(returns[-window:]) * np.sqrt(252)  # Annualized

    def is_change_significant(self, new_fee, old_fee, threshold=0.0001):
        return abs(old_fee - new_fee) / old_fee > threshold