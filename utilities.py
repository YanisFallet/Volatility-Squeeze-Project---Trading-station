import sqlite3 as sq
import pandas as pd
from datetime import datetime

def daily_to_weekly(df : pd.DataFrame):
    return df.resample('W').agg({'Open':'first', 'High':'max', 'Low':'min', 'Close':'last'})
    

def get_stock_data(ticker="MC.PA"):
        with sq.connect("/Users/yanisfallet/sql_server/PEA/action_pea.db") as conn:
            df = pd.read_sql_query(f"SELECT * FROM '{ticker}'", conn)
            df["Date"] = pd.to_datetime(df["Date"])
        return df.set_index("Date")

def is_market_open_europe(date : datetime):
    if date.weekday() >= 5 or date.time() < datetime.time(9,0) or date.time() > datetime.time(17,35):
        return False
    else : return True