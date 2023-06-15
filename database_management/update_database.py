import yfinance as yf
import pandas as pd
import sqlite3
from multiprocessing import Pool
import datetime
import functools

market_extension = {
    "Euronext Paris": "PA",
    "Euronext Brussels": "BR",
    "Euronext Amsterdam": "AS"
}


def compute_transaction_volume(row):
    """Compute the volume of transactions"""
    volume = int(row['Volume'].replace("-", "0"))
    last_price = float(row['last Price'].replace(",", ".").replace("-","0"))
    return volume * last_price

def get_full_symbol(row):
    """Get the full symbol"""
    market = row['Market'].split(",")[0]
    symbol = row['Symbol']
    return f"{symbol}.{market_extension[market]}" if market in market_extension else symbol

def load_symbols(transaction_volume=300000):
    """Loads symbols from the csv file.""" 
    symbols = pd.read_csv('tickers/Euronext_Equities_2023-06-01.csv', sep=';')
    symbols = symbols[symbols["ISIN"].notna()]

    symbols["transaction_volume"] = symbols.apply(compute_transaction_volume, axis=1)
    symbols = symbols[symbols["transaction_volume"] > transaction_volume]
    
    symbols['Full Symbol'] = symbols.apply(get_full_symbol, axis=1)

    return symbols["Full Symbol"].tolist()


def is_weekend(input_date):
    return input_date.weekday() >= 5

def collect_data(symbol):
    """Collects data for a symbol from the last date entered in the table.
    If the table does not exist, it is created and the symbol's history is loaded."""

    with sqlite3.connect("/Users/yanisfallet/sql_server/PEA/action_pea.db") as conn:
        table_exists = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (symbol,)).fetchone() is not None
        
        today = datetime.date.today()        
        now = datetime.datetime.now()       
        is_after_hours = now.time() > datetime.datetime.strptime('17:35', '%H:%M').time()
        
        if not table_exists:
            if not is_after_hours and not is_weekend(today):
                yf.download(symbol, end=(today - pd.DateOffset(days=1)).strftime('%Y-%m-%d')).to_sql(symbol, conn, if_exists='replace')
            else:
                yf.download(symbol).to_sql(symbol, conn)
        else:
            last_date_str = conn.execute(f"SELECT max(Date) FROM '{symbol}'").fetchone()[0]

            if last_date_str:
                last_date = pd.to_datetime(last_date_str)
                start_date = last_date + pd.DateOffset(days=1)
                if start_date.date() <= today and not(is_weekend(start_date) and (is_weekend(today) or (today.weekday() == 0 and not is_after_hours)) and (now - start_date) < pd.Timedelta(days=7)):
                    if is_after_hours:
                        yf.download(symbol, start=start_date.strftime('%Y-%m-%d')).to_sql(symbol, conn, if_exists='append')
                    else:
                        yesterday = today - pd.DateOffset(days=1)
                        yf.download(symbol, start=start_date.strftime('%Y-%m-%d'), end=yesterday.strftime('%Y-%m-%d')).to_sql(symbol, conn, if_exists='append')

def update_data(symbols):
    """Uses multiprocessing to update each table up to today's date."""
    with Pool() as p:
        p.map(collect_data, symbols)
        

def get_date(symbol = "MC.PA"):
    with sqlite3.connect("/Users/yanisfallet/sql_server/PEA/action_pea.db") as conn:
        
        today = datetime.date.today()        
        now = datetime.datetime.now()       
        is_after_hours = now.time() > datetime.datetime.strptime('17:35', '%H:%M').time()
        
        last_date_str = conn.execute(f"SELECT max(Date) FROM '{symbol}'").fetchone()[0]
        last_date = pd.to_datetime(last_date_str)
        start_date = last_date + pd.DateOffset(days=1)
        if start_date.date() <= today and not(is_weekend(start_date) and (is_weekend(today) or (today.weekday() == 0 and not is_after_hours)) and (now - start_date) < pd.Timedelta(days=7)):
            if is_after_hours:
                return start_date, today
            else:
                return start_date, today - pd.DateOffset(days=1)
        return None, None
                        
def optimized_update_data(symbols):
    start_date, end_date = get_date()
    if start_date != None:
        with Pool() as p:
            p.map(functools.partial(yf.download, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d')), symbols)    

if __name__ == '__main__':
    update_data(load_symbols())
