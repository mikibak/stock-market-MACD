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
    import matplotlib.pyplot as plt

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
    for i in range(0, 35):
        signal.iloc[i, 0] = 0
    for i in range(35, 1000):
        signal.iloc[i, 0] = ema(macd, i, 9)
    print(signal)

    plt.subplots_adjust(bottom=0.15)
    plt.xticks(np.arange(0, len(macd) + 1, 10))
    plt.xticks(rotation=30)
    plt.plot(dates, macd, label="MACD")
    plt.plot(dates, signal, label="SIGNAL")
    plt.legend(loc='best')
    plt.show()

    plt.subplots_adjust(bottom=0.15)
    plt.xticks(np.arange(0, len(prices) + 1, 10))
    plt.xticks(rotation=30)
    plt.plot(dates, prices, label="Stock price")
    plt.legend(loc='best')
    plt.show()

    money = 1000
    stocks = 0
    buying = True
    # I should buy or sell when SIGNAL intersects MACD.
    # Days when I trade stocks will be marked as points
    trade_points = pd.DataFrame(index=np.arange(1000), columns=np.arange(1))
    # detect intersection by change in sign of difference
    d = macd - signal
    for i in range(35, 999):
        if float(d.iloc[i]) == 0. or float(d.iloc[i]) * float(d.iloc[i+1]) < 0.:
            trade_points.iloc[i] = macd.iloc[i]
            # crossover at i
            if buying:
                stocks = math.floor(money / prices.iloc[i])
                money -= stocks * prices.iloc[i]
            else:
                money += stocks * prices.iloc[i]
                stocks = 0
            buying = not buying
    print(round(money, 2))

    plt.subplots_adjust(bottom=0.15)
    plt.xticks(np.arange(0, len(macd) + 1, 10))
    plt.xticks(rotation=30)
    plt.plot(dates, trade_points, 'bo', label="Intersections")
    plt.plot(dates, macd, label="MACD")
    plt.plot(dates, signal, label="SIGNAL")
    plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    main()
