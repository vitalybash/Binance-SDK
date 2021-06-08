import hashlib
import hmac
import requests

from urllib.parse import urlencode

apikey = None
secret = None


def create_order(**params):
    servertime = requests.get("https://api.binance.com/api/v1/time").json()
    servertimeint = servertime['serverTime']

    paramsForHash = params.copy()
    paramsForHash['timestamp'] = servertimeint
    paramsForHash = urlencode(paramsForHash)
    hashedsig = hmac.new(secret.encode('utf-8'), paramsForHash.encode('utf-8'),
                         hashlib.sha256).hexdigest()
    params["timestamp"] = servertimeint
    params['signature'] = hashedsig

    userdata = requests.post("https://api.binance.com/api/v3/order",
                             params=params,
                             headers={
                                 "X-MBX-APIKEY": apikey,
                             }
                             )
    return userdata.json()


print(create_order(symbol='ADXBTC',
                   side='SELL',
                   type='MARKET',
                   quantity=1
                   ))
