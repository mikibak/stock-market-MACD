import math


def ema(prices, day, N):
    alpha = 2/(N+1)
    upper_sum = 0
    lower_sum = 0
    for i in range(0, N):
        p = float(prices.iloc[day-i])
        upper_sum += p * math.pow(1 - alpha, i)
        lower_sum += math.pow(1 - alpha, i)
    return upper_sum/lower_sum


def main():

    import pandas as pd
    import numpy as np

    dataframe = pd.read_csv(r'C:\Users\mikolaj\PycharmProjects\StockMarketMACD\stt_us_d.csv')
    dates = dataframe.iloc[:, 0]
    prices = dataframe.iloc[:, 1]

    print(dataframe)

    macd = pd.DataFrame(index=np.arange(1000), columns=np.arange(1))
    for i in range(0, 26):
        macd.iloc[i, 0] = 0
    for i in range(26, 1000):
        ema_26 = ema(prices, i, 26)
        ema_12 = ema(prices, i, 12)
        macd.iloc[i, 0] = ema_12 - ema_26
    print(macd)

    signal = pd.DataFrame(index=np.arange(1000), columns=np.arange(1))
    for i in range(0, 26):
        signal.iloc[i, 0] = 0
    for i in range(26, 1000):
        ema_26 = ema(prices, i, 26)
        ema_12 = ema(prices, i, 12)
        signal.iloc[i, 0] = ema_12 - ema_26
    print(signal)

if __name__ == '__main__':
    main()
