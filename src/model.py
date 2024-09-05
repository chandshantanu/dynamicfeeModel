import joblib
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import numpy as np

class DynamicFeeModel:
    def __init__(self):
        self.model = GradientBoostingRegressor()
        self.scaler = StandardScaler()
        self.data = []
        self.current_fee = 0.003  # Starting with a default fee

    @classmethod
    def load_or_initialize(cls, file_path):
        try:
            return cls.load(file_path)
        except FileNotFoundError:
            return cls()

    def update_and_predict(self, new_data):
        self.data.append(new_data)
        if len(self.data) > 1000:
            self.data = self.data[-1000:]

        X = np.array([[d['price'], d['volume'], d['liquidity'], d['volatility']] for d in self.data])
        y = np.array([d['current_fee'] for d in self.data])

        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

        latest_data = X_scaled[-1].reshape(1, -1)
        predicted_fee = self.model.predict(latest_data)[0]
        
        return np.clip(predicted_fee, 0.0005, 0.01)  # 0.05% to 1%

    def save(self, filename):
        joblib.dump((self.model, self.scaler, self.data, self.current_fee), filename)

    @classmethod
    def load(cls, filename):
        instance = cls()
        instance.model, instance.scaler, instance.data, instance.current_fee = joblib.load(filename)
        return instance