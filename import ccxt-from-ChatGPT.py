import ccxt
import backtrader as bt
import pandas as pd
from datetime import datetime, timedelta
import time

# פונקציה להורדת נתונים היסטוריים
def fetch_historical_data(symbol, timeframe, since):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

# פונקציה להורדת טיק נתונים בזמן אמת
def fetch_live_data(symbol, timeframe):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=1)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

# אסטרטגיית VWAP
class LiveVWAPStrategy(bt.Strategy):
    def __init__(self):
        self.vwap = bt.indicators.WeightedAveragePrice(self.data)
    
    def next(self):
        if self.data.close[0] > self.vwap[0] and not self.position:
            self.buy()
        elif self.data.close[0] < self.vwap[0] and self.position:
            self.sell()

# הגדרת Cerebro והוספת האסטרטגיה
cerebro = bt.Cerebro()
cerebro.addstrategy(LiveVWAPStrategy)

# הגדרת הנתונים ההיסטוריים והוספתם ל-Cerebro
symbol = 'BTC/USDT'
timeframe = '1m'
since = int((datetime.now() - timedelta(days=5)).timestamp() * 1000)  # נתונים מ-5 הימים האחרונים
historical_data = fetch_historical_data(symbol, timeframe, since)
historical_feed = bt.feeds.PandasData(dataname=historical_data)
cerebro.adddata(historical_feed)

# הרצת האסטרטגיה על הנתונים ההיסטוריים
cerebro.run()

# לולאה לעדכון נתונים בזמן אמת
while True:
    # שליפת טיק נתונים בזמן אמת והוספתו ל-Cerebro
    live_data = fetch_live_data(symbol, timeframe)
    live_feed = bt.feeds.PandasData(dataname=live_data)
    cerebro.adddata(live_feed)
    cerebro.run()

    # השהייה של דקה לפני העדכון הבא
    time.sleep(60)
