import requests
import pandas as pd
import time
from io import StringIO

# API клуч (замени го со својот)
API_KEY = "IPDZ574P0F1EGMNL"
BASE_URL = "https://www.alphavantage.co/query"


# Функција за преземање на сите достапни акции
def get_all_stocks():
    params = {
        "function": "LISTING_STATUS",
        "apikey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        csv_data = response.text
        df = pd.read_csv(StringIO(csv_data))  # Конвертирање на CSV во DataFrame
        df = df[df["status"] == "Active"]  # Задржуваме само активни акции
        return df
    else:
        print("Грешка при преземање на податоци:", response.status_code)
        return None


# Функција за преземање на податоци за одредена акција
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
        print(f"Грешка при земање податоци за {symbol}: {response.status_code}")
        return None


# Функција за обработка на податоците
def process_stock_data(data, symbol):
    if data:
        time_series = data.get('Time Series (5min)', {})
        if time_series:
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df = df.astype(float)  # Конвертирање на податоците во float
            df['symbol'] = symbol
            return df
    return None


# Главна функција
def main():
    print("Преземам листа на сите активни акции...")
    stock_df = get_all_stocks()

    if stock_df is None:
        print("Не можам да ја преземам листата на акции.")
        return

    stock_symbols = stock_df["symbol"].tolist()  # Листа со сите симболи
    print(f"Пронајдени {len(stock_symbols)} активни акции.")

    all_data = []

    for symbol in stock_symbols:  # Ограничи на првите 10 акции за тестирање
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

        time.sleep(60)  # Чекање помеѓу барањата (Alpha Vantage има rate limit)

    if all_data:
        final_df = pd.concat(all_data, axis=0)
        print("\nКонечни податоци:\n", final_df.head())
        final_df.to_csv("stock_dataa.csv", index=False)
        print("Податоците се зачувани во stock_dataa.csv")


if __name__ == "__main__":
    main()