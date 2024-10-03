import yfinance as yf


class CryptoDataFetcher:
    def __init__(self, cryptos):
        self.cryptos = cryptos

    def fetch_prices(self, period="1d", interval="5m"):
        data = {}
        for crypto in self.cryptos:
            ticker = yf.Ticker(crypto)
            data[crypto] = ticker.history(period=period, interval=interval)
        return data
