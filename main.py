from components.crypto_dashboard import CryptoDashboard

if __name__ == '__main__':
    cryptos = ['BTC-USD', 'ETH-USD', 'USDT-USD', 'BNB-USD',
               'SOL-USD', 'USDC-USD', 'XRP-USD', 'STETH-USD']
    dashboard = CryptoDashboard(cryptos)
    dashboard.run()
