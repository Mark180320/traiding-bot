import time
from datetime import datetime

from binance import Client
import pandas as pd

from task1 import get_determ

# апи ключ и секрет нужный для подключения к Binance API
api_key = ''
api_secret = ''
client = Client(api_key, api_secret)


# Функция для получения цен
def get_coin(symbol, limit):
    # интервал обновления данных по цене можно менять, в данном случае раз в минуту
    data = client.get_klines(symbol=symbol, interval="1m", limit=limit)

    df = pd.DataFrame()

    # упаковываем в датафрейм для облегчения дальнейшей работы
    for candle in range(limit):
        date_time = datetime.fromtimestamp(data[candle][0] / 1e3)
        close_price = float(data[candle][4])
        new_df = pd.DataFrame({'Time': [date_time], f'{symbol}': [close_price]})
        df = pd.concat([df, new_df], ignore_index=True)

    return df


def get_change(symbol):
    # Получаем цену
    pr = get_coin(symbol, limit=60)

    # Определяем минимум и максимум
    max_pr = pr[symbol].max()
    min_pr = pr[symbol].min()

    pr_change = (max_pr - min_pr) / min_pr

    # Получаем изменение цены с учетом коэффициента детерминации
    if pr_change >= (0.01 / (1 - get_determ())):
        return True

    return False


while True:
    if get_change('ETHUSDT'):
        print('Произошло изменение в цене более чем на 1%')
    else:
        print('За час не было изменений в цене')

    time.sleep(60)
