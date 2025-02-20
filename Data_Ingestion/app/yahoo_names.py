import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random


def setup_driver():
    """
    Sets up the Selenium WebDriver with necessary options and returns the driver.
    """

    options = Options()
    options.headless = False  # Change to True if you don't want the browser to open
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(180)  # Зголеми на 180 секунди (3 минути)

    return driver


def get_stock_symbols_from_page(driver, url):
    """
    Scrapes stock symbols from a given Yahoo Finance URL using Selenium.

    :param driver: The Selenium WebDriver instance
    :param url: The URL to scrape stock symbols from
    :return: A list of stock symbols (tickers)
    """
    try:
        driver.get(url)  # ✅ Пробавме да ја отвориме страницата
    except Exception as e:
        print(f"⚠ Грешка при вчитување на {url}: {e}")
        return []  # ✅ Ако не може да се отвори, прескокнува

    try:
        # Wait until stock elements are loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.symbol.yf-1m808gl"))
        )
    except Exception as e:
        print(f"⚠ Timeout: Could not find stock table on {url} - {e}")
        return []

    # Find all stock symbols
    stock_elements = driver.find_elements(By.CSS_SELECTOR, "span.symbol.yf-1m808gl")

    # Extract and return text
    stock_symbols = [elem.text.strip() for elem in stock_elements if elem.text.strip()]
    return stock_symbols



def scrape_all_stock_symbols():
    """
    Scrapes stock symbols from Yahoo Finance's 'Most Active', 'Top Gainers', and 'Top Losers' pages.
    Uses pagination to get all available symbols, stopping at a maximum of start=300.
    """
    base_urls = [
        "https://finance.yahoo.com/markets/stocks/most-active",
        "https://finance.yahoo.com/markets/stocks/gainers",
        "https://finance.yahoo.com/markets/stocks/losers"
    ]

    driver = setup_driver()  # Setup Selenium WebDriver
    all_stock_symbols = []

    for base_url in base_urls:
        start = 0  # Start pagination from 0

        while start <= 300:  # ✅ Ограничување: ако start е поголем од 300, оди на следниот URL
            paginated_url = f"{base_url}/?start={start}&count=100"
            print(f"Scraping {paginated_url}...")

            stock_symbols = get_stock_symbols_from_page(driver, paginated_url)

            if not stock_symbols:
                print(f"⚠ No more stock symbols found on {paginated_url}. Stopping pagination.")
                break  # Stop if no new symbols are found

            all_stock_symbols.extend(stock_symbols)
            start += 100  # Move to the next page

            time.sleep(2)  # Small delay to avoid detection

    driver.quit()  # Close the Selenium WebDriver

    # Save data to CSV
    with open("all_stock_symbols.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Stock Symbol"])  # Writing header
        for symbol in all_stock_symbols:
            writer.writerow([symbol])

    print(f"✅ Scraping complete! {len(all_stock_symbols)} stock symbols saved to 'all_stock_symbols.csv'.")


if __name__ == "__main__":
    scrape_all_stock_symbols()
