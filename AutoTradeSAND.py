import time
import pyupbit
import datetime

access = ""
secret = ""

# SAND 코인, MA를 20으로 변경, 시간텀 240분 변경

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=1)
    start_time = df.index[0]
    return start_time

def get_ma20(ticker):
    """20일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=20)
    ma20 = df['close'].rolling(20).mean().iloc[-1]
    return ma20

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-SAND")
        end_time = start_time + datetime.timedelta(minutes=240)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-SAND", 0.3)
            ma20 = get_ma20("KRW-SAND")
            current_price = get_current_price("KRW-SAND")
            if target_price < current_price :  # and ma20 < current_price
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-SAND", krw*0.9995)
        else:
            SAND = get_balance("SAND")
            if SAND > 0.00008:
                upbit.sell_market_order("KRW-SAND", SAND*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
