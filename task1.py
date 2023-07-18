from binance.client import Client
import pandas as pd


# апи ключ и секрет нужный для подключения к Binance API
api_key = ''
api_secret = ''
client = Client(api_key, api_secret)


# Функция для получения свечей
def get_klines(symbol, interval, limit):
    # Получаем выборку свечей
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)

    # Для удобства преобразовываем данные в DataFrame
    dataframe = pd.DataFrame(klines, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                                              'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
                                              'Taker buy quote asset volume', 'Ignore'])

    dataframe['Open time'] = pd.to_datetime(dataframe['Open time'], unit='ms')
    dataframe['Close time'] = pd.to_datetime(dataframe['Close time'], unit='ms')
    dataframe = dataframe.set_index('Close time')
    dataframe = dataframe[['Open', 'High', 'Low', 'Close', 'Volume']]
    dataframe = dataframe.astype('float')

    return dataframe


# Функция для получения коэффициента детерминации который показывает влияние BTCUSDT на ETHUSDT
def get_determ():
    # Получаем 100 свеч фьючерса ETHUSDT и BTCUSDT с интервалом в 1 минуту
    eth = get_klines('ETHUSDT', Client.KLINE_INTERVAL_1MINUTE, 100)
    btc = get_klines('BTCUSDT', Client.KLINE_INTERVAL_1MINUTE, 100)

    # Рассчитываем коэффициент корреляции
    corr = eth.corrwith(btc)

    # Рассчитаем долю движения ETHUSDT, которая вызвана BTCUSDT с помощью коэффициента детерминации
    cf_determ = corr['Close'] ** 2

    return cf_determ
