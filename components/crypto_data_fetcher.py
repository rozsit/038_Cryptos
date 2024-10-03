import yfinance as yf


class CryptoDataFetcher:
    def __init__(self, cryptos):
        self.cryptos = cryptos

    def fetch_prices(self, period="1d", interval="5m"):
        data = {crypto: yf.Ticker(crypto).history(
            period=period, interval=interval) for crypto in self.cryptos}

        return data
