import sqlite3 as sq
import pandas as pd
import numpy as np

l = ["VolatilitySqueeze"]


class VolatilitySqueeze:
    def __init__(self, db_path = "/Users/yanisfallet/sql_server/PEA/action_pea.db", load_factor=1, window=21):
        self.db_path = db_path
        self.load_factor = load_factor
        self.window = window

    @staticmethod
    def weighted_mean(data):
        weights = np.arange(1, data.shape[0]+1)
        return np.sum(data * weights) / np.sum(weights)

    @staticmethod
    def volatility_metric(data, window):
        intra_day_vol = data["High"] - data["Low"]
        avg_idv = intra_day_vol.rolling(window).apply(VolatilitySqueeze.weighted_mean, raw=True)
        return intra_day_vol/avg_idv

    @staticmethod
    def compute_ema(data, window):
        return data.ewm(span=window, adjust=True).mean()

    @staticmethod
    def compute_sma(data, window):
        return data.rolling(window).mean()

    def screener(self):
        """Screen for volatility metrics for all tables in a given database."""
        # Connect to the database
        with sq.connect(self.db_path) as conn:
            # Get list of table names
            tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)["name"].tolist()
            vol_metrics = {}
            for table in tables:
                df = pd.read_sql_query(f"""
                                    SELECT * FROM (
                                        SELECT * FROM '{table}' ORDER BY Date DESC LIMIT {self.load_factor*100}
                                    ) sub
                                    ORDER BY Date ASC
                                    ;""", conn)
                df["Date"] = pd.to_datetime(df["Date"])
                df = df.set_index("Date")
                df_weekly = df.resample('W').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'})
                
                weekly_ema = self.compute_ema(df_weekly["Close"][-self.window:], 3)
                weekly_sma = self.compute_sma(df_weekly["Close"][-self.window:], 7)
                
                if weekly_ema[-1] > weekly_ema[-2] or weekly_ema[-1] > weekly_sma[-1]:
                    vol_metrics[table] = self.volatility_metric(df, self.window)[-1]
                    
        return {k: v for k, v in sorted(vol_metrics.items(), key=lambda item: item[1])}

if __name__ == "__main__":
    path = "/Users/yanisfallet/sql_server/PEA/action_pea.db"
    vs = VolatilitySqueeze(path)
    print(vs.screener())
    