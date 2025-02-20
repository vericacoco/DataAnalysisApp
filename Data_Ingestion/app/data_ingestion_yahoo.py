import yfinance as yf
import pandas as pd


def fetch_stock_data(tickers):
    """Fetch comprehensive stock data for a list of tickers from Yahoo Finance."""
    all_data = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period="30d")
            info = stock.info

            # Extract last closing price
            last_price = history["Close"].iloc[-1] if not history.empty else None

            # Extract financials safely
            financials = stock.financials if not stock.financials.empty else None
            revenue = financials.loc["Total Revenue"][
                0] if financials is not None and "Total Revenue" in financials.index else None
            net_income = financials.loc["Net Income"][
                0] if financials is not None and "Net Income" in financials.index else None

            # Additional stock data
            data = {
                "Ticker": ticker,
                "Last Price": last_price,
                "Market Cap": info.get("marketCap"),
                "PE Ratio": info.get("trailingPE"),
                "EPS": info.get("trailingEps"),
                "Revenue": revenue,
                "Net Income": net_income,
                "Dividend Yield": info.get("dividendYield"),
                "52 Week High": info.get("fiftyTwoWeekHigh"),
                "52 Week Low": info.get("fiftyTwoWeekLow"),
                "Beta": info.get("beta"),
                "Volume": info.get("volume"),
                "Average Volume": info.get("averageVolume"),
                "Sector": info.get("sector"),
                "Industry": info.get("industry"),
            }
            all_data.append(data)

        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

    return pd.DataFrame(all_data)

# Функција за обработка на податоците
def process_stock_data(data, symbol):
    """Process the stock data and return it as a pandas DataFrame."""
    if data:
        time_series = data.get('Time Series (5min)', {})
        if time_series:
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df = df.astype(float)  # Convert data to float
            df['symbol'] = symbol
            return df


def main():
    tickers = [

    "IWX", "IWJ", "IWK",
    "MGK", "MGV", "MTUM", "QUAL", "SIZE", "USMV", "VOT", "VOE", "VBR", "VHT",
    "VGT", "VDE", "VIS", "VCR", "VDC", "VAW", "VNQ", "VNQI", "VXUS", "VEU",
    "VEA", "VWO", "EWJ", "EWG", "EWU", "EWL", "EWD", "EWO", "EWK", "EWI",
    "EWQ", "EWN", "EWS", "EWH", "EWM", "EWT", "EWC", "EZA", "RSX", "EWZ",
    "BHP", "RIO", "PTR", "CHL", "SNP", "TM", "NVS", "SAP", "BIDU", "NTES",
        "SMCI", "NVDA", "INTC", "RGTI", "PLTR", "GRAB", "LCID", "TSLA", "RXRX", "HIMS",
    "BBAI", "BBD", "SOUN", "F", "GOLD", "BAC", "NIO", "BTG", "BABA", "SOFI",
    "BTE", "RIG", "ACHR", "WBD", "VALE", "COMP", "OXY", "PFE", "TDOC", "APLD",
    "BB", "NU", "PSLV", "AMD", "AAPL", "IQ", "T", "RIVN", "CELH", "HOOD",
    "ANET", "AMZN", "VRN", "PCG", "IONQ", "VNET", "AAL", "LYFT", "MARA", "DVN",
    "MSFT", "GOOG", "META", "WMT", "TSM", "TSLA", "AAPL", "NVDA", "ARM", "XOM",
    "QCOM", "RIVN", "AVGO", "CDNS", "COF", "LI", "SHOP", "TME", "BA", "ORCL",
    "FCX", "C", "DIS", "BILI", "MRNA", "JD", "NEM", "KHC", "NEE", "CSCO",
    "SLB", "MDT", "GDS", "NCLH", "CVS", "COIN", "DAL", "HAL", "KMI", "DELL",
    "LUV", "NXPI", "XPEV", "AUR", "MRVL", "CSX", "INFY", "EQT", "FOUR", "KRYS",
    "PEN", "RBA", "VKTX", "SSRM", "HCM", "STM", "MCHP", "ADI", "CRK", "ENLT",
    "NPO", "HBM", "CNK", "WRD", "HHH", "OKLO", "AXON", "BRK-B", "UEC", "CLVT",
    "AGNC", "MU", "VZ", "CMCSA", "AMCR", "MSTR", "RKLB", "HBAN", "ET", "DKNG",
    "SNAP", "ON", "CMG", "LRCX", "UBER", "CLSK", "MRK", "TEVA", "ABEV", "CE",
    "UMC", "IREN", "ETSY", "QS", "NKE", "NGD", "PARA", "APPN", "ITUB", "CNH",
    "HL", "TEM", "GOOGL", "RIOT", "JBLU", "NBIS", "CDE", "KGC", "IBRX", "PR",
    "GILD", "GM", "F", "TSMC", "STLA", "HOOD", "WFC", "HBI", "UPST", "KRYS",
    "MIRM", "APG", "CRL", "FNMA", "UPWK", "TEO", "GSAT", "MOH", "CART", "MIR",
    "ASTS", "POWI", "CPRI", "MRUS", "DIOD", "PGNY", "MTRN", "TMDX", "ESI", "FTAI",
    "XIACF", "MRX", "LNW", "CSGP", "GPOR", "KTB", "GKOS", "ALGM", "TOELY", "TFX",
    "FMCC", "VSH", "IEP", "RDNT", "EXEL", "FUN", "VIST", "RNECY", "GIL", "AEIS",
    "DFS", "RGEN", "CW", "MMYT", "VCYT", "CTRA", "SAABY", "CNC", "GLBE", "WING",
    "PHG", "PSN", "CAVA", "LPX", "IESC", "DAR", "HRMY", "JBSAY", "ALVO", "VTMX",
    "PPERY", "POWL", "GLNCY", "FLS", "IOSP", "MPNGY", "TOL", "WIX", "S", "ASAN",
    "ALAB", "RNG", "ZETA", "W", "MOD", "IFF", "CLH", "SG", "BASFY", "AFRM", "FROG",
    "KSPI", "AMR", "ANGPY", "ESAB", "BTSG", "AU", "VSCO", "HCMLY", "CRDO", "RBRK",
    "RNW", "SNPS", "CSAN", "MBLY", "WGS", "MANU", "SAIA", "CARG", "LMND", "YETI",


    "TXN", "PYPL", "ADBE", "NFLX", "ABNB", "NOW", "SNOW", "U", "PANW", "TEAM",
    "SHOP", "ZI", "DDOG", "FSLY", "MDB", "DOCN", "CRWD", "SPLK", "BILL", "TWLO",
    "OKTA", "ZS", "RBLX", "FVRR", "UPWK", "TTD", "ROKU", "FUBO", "TQQQ", "SQQQ",
    "ARKK", "ARKG", "SOXL", "SOXS", "LABU", "LABD", "TECL", "SPXL", "SPXS", "XLF",
    "XLY", "XLK", "XLC", "XLI", "XLV", "XLP", "XLE", "XLU", "XLB", "XME",
    "GDX", "GDXJ", "SLV", "GLD", "TLT", "HYG", "LQD", "SPY", "QQQ", "DIA",
    "IWM", "VOO", "VTI", "BND", "VXUS", "VWO", "VEA", "SCHD", "SPHD", "JEPI",
    "SPYD", "VYM", "DVY", "SDY", "HDV", "DGRW", "PDBC", "USO", "UNG", "UGA",
    "UCO", "SCO", "XOP", "OIH", "FENY", "IEO", "FCG", "KOLD", "BOIL", "NUGT",
    "DUST", "TNA", "TZA", "URTY", "DRN", "DRV", "SRTY", "SPXS", "UPRO", "SPXU",
    "QQQJ", "QQQM", "SPYG", "SPYD", "VUG", "VTV", "IVV", "IJK", "IJS", "IJT",
    "IWN", "IWO", "IWF", "IWR", "IWM", "IWY", "IWZ"
    ]

    df = fetch_stock_data(tickers)
    print(df)
    df.to_csv("stock_data_yahoo.csv", mode='a', header=False, index=False)


if __name__ == "__main__":
    main()
