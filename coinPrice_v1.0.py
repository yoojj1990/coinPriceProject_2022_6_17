import sys
import time

import pyupbit
import requests
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#   / 코인 선택  /  coin_comboBox
#   /  코인 종류  /  coinTicker_label
# trade_price  / 현재가 / coinPrice_label
# signed_change_rate   / 변화율 / coinChang_label
# acc_trade_volume_24h  / 24시간 거래량  / acc_trade_volume_label
# acc_trade_price_24h  / 24시간 누적 거래대금 / acc_trade_price_label
# trade_volume  / 최근 거래량 / trade_volume_label
# high_price  / 고가 / high_price_label
# low_price  / 저가 / low_price_label
# prev_closing_price  / 종가 / prev_closing_price_label

from_class = uic.loadUiType("ui/coinPriceUi.ui")[0]

class CoinViewThread(QThread):
    # 시그널 함수 정의
    coinDataSent = pyqtSignal(float, float, float, float, float, float, float, float)

    def __init__(self, ticker):  # mainWindow에서 쓰레드 클레스의 변수를 전달
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):
        # 업비트 정보 API 호출 반복
        while self.alive:
            url = "https://api.upbit.com/v1/ticker"

            param = {"markets": f"KRW-{self.ticker}"}  # 받아온 티커값을 파리미터 값으로 설정

            response = requests.get(url, params=param)

            upbitResult = response.json()

            trade_price = upbitResult[0]['trade_price']  # 현재가 / coinPrice_label
            signed_change_rate = upbitResult[0]['signed_change_rate']  # 변화율 / coinChang_label
            acc_trade_volume_24h = upbitResult[0]['acc_trade_volume_24h']  # 24시간 거래량  / acc_trade_volume_label
            acc_trade_price_24h = upbitResult[0]['acc_trade_price_24h']  # 24시간 누적 거래대금 / acc_trade_price_label
            trade_volume = upbitResult[0]['trade_volume']  # 최근 거래량 / trade_volume_label
            high_price = upbitResult[0]['high_price']  # 고가 / high_price_label
            low_price = upbitResult[0]['low_price']  # 저가 / low_price_label
            prev_closing_price = upbitResult[0]['prev_closing_price']  # 종가 / prev_closing_price_label

            # 시그널 슬롯에 코인 정보 보내기
            self.coinDataSent.emit(float(trade_price),
                                   float(signed_change_rate),
                                   float(acc_trade_volume_24h),
                                   float(acc_trade_price_24h),
                                   float(trade_volume),
                                   float(high_price),
                                   float(low_price),
                                   float(prev_closing_price))

            time.sleep(1)  # api 호출 딜레이(1초마다 업비트 정보 호출)

    def close(self):
        self.alive = False



class MainWindow(QMainWindow, from_class):
    def __init__(self, ticker="BTC"):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("BitCoin Price Overview")
        self.setWindowIcon(QIcon("icons/bitcoin.png"))
        self.statusBar().showMessage("ver 0.5")
        self.ticker = ticker

        self.cvt = CoinViewThread(ticker)  # 코인 정보를 가져오는 쓰레드 클래스를 맴버객체로 선언
        self.cvt.coinDataSent.connect(self.fillCoinData) # 쓰레드 시그널에서 온 데이터를 받아줄 슬롯함수를 연결
        self.cvt.start()  # 쓰레드 클래스의 run()를 호출(함수시작)
        self.comboBox_setting()  # 콤보박스 초기화 함수 호출

    def comboBox_setting(self):  # 코인리스트 콤보박스 셋팅
        ticker_list = pyupbit.get_tickers(fiat="KRW")  # 모든 코인 리스트 불러오기

        # 필요없는 부분 빼고 리스트에 넣기
        coin_list = []
        for ticker in ticker_list:
            coin_list.append(ticker[4:10])  # ticker 에서 'KRW-' 를 빼고 리스트에 추가

        # coin_list = ['BTC', 'ETH', 'XRP', 'IOST' ,'NEAR']  # 원하는 리스트 목록 만들기

        # 코인 리스트 정렬
        coin_list.remove('BTC')  # 리스트에서 특정 값 제거
        coin_list1 = ['BTC']  # 가장 위에 놓기 위해 하나 빼기
        coin_list2 = sorted(coin_list)  # BTC를 뺀 리스트를 정렬

        coin_list3 = coin_list1 + coin_list2   # BTC를 가장 위에 두고 나마저 정렬된 리스트 추가

        self.coin_comboBox.addItems(coin_list3)  # 코인(ticker) 리스트를 콤보박스에 추가

        self.coin_comboBox.currentIndexChanged.connect(self.coin_select_combobox)  # 콤보박스의 값이 변경되었을때 연결된 함수 실행

    def coin_select_combobox(self):
        cion_ticker = self.coin_comboBox.currentText()  # 콤보박스에서 선택된 티커 불러오기
        self.ticker = cion_ticker  # 맴버변수인 티커의 값을 콤보박스에서 선택된 티커로 변경
        self.coinTicker_label.setText(cion_ticker)  # 콤보박스에서 선택된 티커로 코인 레이블을 셋팅

        self.cvt.close()  # 현재 실행되고있는 쓰래드를 정지시킴(while 종료)

        self.cvt = CoinViewThread(cion_ticker)  # 코인 정보를 가져오는 쓰레드 클래스를 맴버객체로 선언
        self.cvt.coinDataSent.connect(self.fillCoinData)  # 쓰레드 시그널에서 온 데이터를 받아줄 슬롯함수를 연결
        self.cvt.start()  # 쓰레드 클래스의 run()를 호출(함수시작)


    # 쓰레드 클래스에서 보내준 데이터를 받아주는 슬롯 함수
    def fillCoinData(self, trade_price, signed_change_rate, acc_trade_volume_24h,
                     acc_trade_price_24h, trade_volume, high_price, low_price, prev_closing_price):
        self.coinPrice_label.setText(f"{trade_price:,.0f}원")  # 코인 현재가격
        self.coinChang_label.setText(f"{signed_change_rate:+.2f}%")  # 가격 변화율
        self.acc_trade_volume_label.setText(f"{acc_trade_volume_24h:,.4f} {self.ticker}")  # 24시간 거래량
        self.acc_trade_price_label.setText(f"{acc_trade_price_24h:,.0f}원")  # 24시간 누적 거래대금
        self.trade_volume_label.setText(f"{trade_volume:.8f}  {self.ticker}")  # 최근 거래량
        self.high_price_label.setText(f"{high_price:,.0f}원")  # 당일 고가
        self.low_price_label.setText(f"{low_price:,.0f}원")  # 당일 저가
        self.prev_closing_price_label.setText(f"{prev_closing_price:,.0f}원")  # 전일 종가

        self.__updateStyle()


    def __updateStyle(self):
        if '-' in self.coinChang_label.text():
            # 원하는 label, button 등의 위젯 스타일시트 정의
            self.coinChang_label.setStyleSheet("background-color:blue;color:white")
            self.coinPrice_label.setStyleSheet("color:blue")

        else:
            self.coinChang_label.setStyleSheet("background-color:red;color:white")
            self.coinPrice_label.setStyleSheet("color:red")






if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())