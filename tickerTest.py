# 티커 테스트
# import requests
# import pyupbit
#
# url = "https://api.upbit.com/v1/market/all?isDetails=false"
#
# headers = {"Accept": "application/json"}
#
# response = requests.get(url, headers=headers)
#
# print(response.text)
#
# ticker_list = pyupbit.get_tickers()
# print(ticker_list)


# 티커 리스트 뽑기
import pyupbit

ticker_list = pyupbit.get_tickers(fiat="KRW")
print(ticker_list)

coin_list = []

for ticker in ticker_list:
    #print(ticker[4:10])
    coin_list.append(ticker[4:10])

print(coin_list)