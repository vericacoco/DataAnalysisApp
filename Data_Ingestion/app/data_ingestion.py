import requests
import time
import pandas as pd



# Your API key from Alpha Vantage
API_KEY = "IPDZ574P0F1EGMNL"
BASE_URL = "https://www.alphavantage.co/query"

# Large list of stock symbols (expand this list based on your needs)
stock_symbols = [
    'AAPL', 'GOOG', 'AMZN', 'MSFT', 'TSLA', 'FB', 'NFLX', 'NVDA', 'SPY', 'V', 'BABA',
    'INTC', 'AMD', 'TSM', 'DIS', 'BA', 'CSCO', 'ORCL', 'IBM', 'WMT', 'GS', 'PYPL', 'MS',
    'XOM', 'CVX', 'GE', 'C', 'JPM', 'MCD', 'KO', 'PEP', 'NKE', 'VZ', 'T', 'MMM', 'UNH',
    'JNJ', 'PFE', 'MRK', 'AMGN', 'BMY', 'ABBV', 'GILD', 'LLY', 'MRNA', 'ZTS', 'BAX',
    'ABT', 'MDT', 'BDX', 'SYK', 'SPG', 'CCI', 'PLD', 'AMT', 'EXR', 'PSA', 'AVB', 'EQR',
    'DHI', 'LEN', 'TOL', 'PHM', 'X', 'NUE', 'STLD', 'CLF', 'FSR', 'LI', 'NKLA', 'RIVN',
    'F', 'GM', 'HMC', 'TM', 'KHC', 'SYY', 'HRL', 'ADM', 'GIS', 'CHD', 'CL', 'PG', 'KO'
]



# Function to fetch stock data
def get_stock_data(symbol):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '5min',
        'apikey': API_KEY
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {symbol}: {response.status_code}")
        return None


# Функција за обработка на податоците користејќи pandas
def process_stock_data(data, symbol):
    if data:
        time_series = data.get('Time Series (5min)', {})
        if time_series:
            # Претворање во pandas DataFrame за полесна обработка
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df = df.astype(float)  # Претворање на податоците во тип float
            df['symbol'] = symbol
            return df
    return None





# Главна функција
def main():
    all_data = []

    for symbol in stock_symbols:
        print(f"\nСобирање податоци за акцијата: {symbol}")
        stock_data = get_stock_data(symbol)

        if stock_data:
            processed_data = process_stock_data(stock_data, symbol)
            if processed_data is not None:
                all_data.append(processed_data)
                print(f"Податоци за {symbol} успешно собрани.")

            else:
                print(f"Не можам да ги обработам податоците за {symbol}.")
        else:
            print(f"Не можам да ги добијам податоците за {symbol}.")

        # Чекање помеѓу барањата
        time.sleep(60)

    # Конкатенирање на сите податоци во еден DataFrame
    if all_data:
        final_df = pd.concat(all_data, axis=0)
        print("\nКонечни податоци:\n", final_df.head())


if __name__ == "__main__":
    main()
