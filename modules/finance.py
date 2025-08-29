import requests

def get_crypto_price(symbol="BTC", currency="USD"):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies={currency}"
        data = requests.get(url).json()
        return f"💰 {symbol.upper()} Price: {data[symbol][currency.lower()]} {currency}"
    except:
        return "⚠️ Could not fetch crypto price."

def get_stock_price(symbol="AAPL"):
    try:
        url = f"https://financialmodelingprep.com/api/v3/quote-short/{symbol}?apikey=demo"
        data = requests.get(url).json()
        return f"📈 {symbol.upper()} Price: {data[0]['price']}"
    except:
        return "⚠️ Could not fetch stock price."
