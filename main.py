from components.crypto_dashboard import CryptoDashboard

if __name__ == '__main__':
    cryptos = ['BTC-USD', 'WBTC-USD', 'WSTETH-USD', 'WETH-USD',
               'STETH-USD', 'ETH-USD', 'BNB-USD', 'BCH-USD']
    dashboard = CryptoDashboard(cryptos)
    dashboard.run()
