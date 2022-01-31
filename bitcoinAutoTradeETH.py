import time
import pyupbit
import datetime

access = ""
secret = ""

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)  #ohlcv 조회시 일봉(day)로 하면 그날의 시작시간나옴
    start_time = df.index[0]  #위에서 받은 ohlcv의 가장첫번째가 시작시간이고 이걸 start time으로 받음
    return start_time

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
        now = datetime.datetime.now()  #현재시간 받기
        start_time = get_start_time("KRW-ETH")   #시작시간 09:00 받기 get start time 함수활용
        end_time = start_time + datetime.timedelta(days=1)   ##끝나느니간 = 시작시간 09:00 + 1일

        # 9:00 < 현재 < #8:59:50 
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-ETH", 0.3)
            current_price = get_current_price("KRW-ETH")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-ETH", krw*0.9995)
        else:
            btc = get_balance("ETH")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-ETH", btc*1)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
