import requests

url = "https://api.upbit.com/v1/ticker"

param = {"markets":"KRW-BTC"}

response = requests.get(url, params=param)

upbitResult = response.json()

print(upbitResult[0]['trade_price'])  # 현재가 / coinPrice_label
print(upbitResult[0]['signed_change_rate'])   # 변화율 / coinChang_label
print(upbitResult[0]['acc_trade_volume_24h'])  # 24시간 거래량  / acc_trade_volume_label
print(upbitResult[0]['acc_trade_price_24h'])  # 24시간 누적 거래대금 / acc_trade_price_label
print(upbitResult[0]['trade_volume'])  # 최근 거래량 / trade_volume_label
print(upbitResult[0]['high_price'])  # 고가 / high_price_label
print(upbitResult[0]['low_price'])  # 저가 / low_price_label
print(upbitResult[0]['prev_closing_price'])  # 종가 / prev_closing_price_label
