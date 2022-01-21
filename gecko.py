import talib
import numpy
import requests
import json
import time
class Gecko:
    def __init__(self):
        pass    
    
    def get_last_price(self,contract):
        url = 'https://api.coingecko.com/api/v3/simple/token_price/binance-smart-chain?contract_addresses='+contract+'&vs_currencies=usd'
        last_price = requests.get(url)

        last_price = json.loads(last_price.text)
        last_price = float(last_price[contract]['usd'])
        return last_price
        
    def get_last_rsi(self,id,contract):
        
        url = 'https://api.coingecko.com/api/v3/coins/'+id+'/ohlc?vs_currency=usd&days=30'
        market_data = requests.get(url)

        market_data = json.loads(market_data.text)
        prices = []
        for i in market_data:
            prices.append(float(i[4]))
        prices.pop()
        time.sleep(1)
        prices.append(self.get_last_price(contract))

        last_RSI = talib.RSI(numpy.asarray(prices), 14)[-1]
        return last_RSI