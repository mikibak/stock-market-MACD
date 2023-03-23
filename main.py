import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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

    dataframe = pd.read_csv(r'C:\Users\mikolaj\PycharmProjects\StockMarketMACD\stt_us_d.csv')
    dates = dataframe.iloc[:, 0]
    prices = dataframe.iloc[:, 1]

    print('All data:')
    print(dataframe)

    macd = pd.DataFrame(index=np.arange(dates.size), columns=np.arange(1))
    for i in range(0, 26):
        macd.iloc[i, 0] = 0
    for i in range(26, dates.size):
        ema_26 = ema(prices, i, 26)
        ema_12 = ema(prices, i, 12)
        macd.iloc[i, 0] = ema_12 - ema_26
    print('MACD:')
    print(macd)

    signal = pd.DataFrame(index=np.arange(dates.size), columns=np.arange(1))
    for i in range(0, 35):
        signal.iloc[i, 0] = 0
    for i in range(35, dates.size):
        signal.iloc[i, 0] = ema(macd, i, 9)
    print('SIGNAL:')
    print(signal)

    money = 1000
    stocks = 0
    # I should buy or sell when SIGNAL intersects MACD.
    # Days when I trade stocks will be marked as points
    trade_points = pd.DataFrame(index=np.arange(dates.size), columns=np.arange(1))
    sell_dates = pd.DataFrame(index=np.arange(dates.size), columns=np.arange(1))
    buy_dates = pd.DataFrame(index=np.arange(dates.size), columns=np.arange(1))
    money_over_time = pd.DataFrame(index=np.arange(dates.size), columns=np.arange(1))
    # detect intersection by change in sign of difference
    d = macd - signal
    for i in range(35, dates.size-1):
        if float(d.iloc[i]) == 0. or float(d.iloc[i]) * float(d.iloc[i+1]) < 0.:
            trade_points.iloc[i] = macd.iloc[i]
            # crossover at i
            if float(d.iloc[i]) < 0:
                stocks = math.floor(money / prices.iloc[i])
                money -= stocks * prices.iloc[i]
                buy_dates.iloc[i] = i
            else:
                money += stocks * prices.iloc[i]
                stocks = 0
                sell_dates.iloc[i] = i
                money_over_time.iloc[i] = money
    print('Money: ' + str(round(money, 2)))

    plt.title("MACD and SIGNAL")
    plt.xlabel('Date')
    plt.ylabel('Index value')
    plt.subplots_adjust(bottom=0.25)
    plt.xticks(np.arange(0, len(macd) + 1, 10))
    plt.xticks(rotation=30)
    plt.plot(dates, macd)
    plt.plot(dates, macd, label="MACD")
    plt.plot(dates, signal, label="SIGNAL")
    plt.legend(loc='best')
    plt.show()

    plt.title("Stock prices")
    plt.xlabel('Date')
    plt.ylabel('Stock value')
    plt.subplots_adjust(bottom=0.25)
    plt.xticks(np.arange(0, len(prices) + 1, 10))
    plt.xticks(rotation=30)
    plt.plot(dates, prices, label="Stock price")
    plt.legend(loc='best')
    plt.show()

    plt.title("MACD, SIGNAL and their intersections")
    plt.xlabel('Date')
    plt.ylabel('Index value')
    plt.subplots_adjust(bottom=0.25)
    plt.xticks(np.arange(0, len(macd) + 1, 10))
    plt.xticks(rotation=30)
    plt.plot(dates, trade_points, 'bo', label="Intersections")
    plt.plot(dates, macd, label="MACD")
    plt.plot(dates, signal, label="SIGNAL")
    plt.legend(loc='best')
    plt.show()

    plt.title("Stock prices and buying/selling dates")
    plt.xlabel('Date')
    plt.ylabel('Stock value')
    plt.subplots_adjust(bottom=0.25)
    plt.xticks(np.arange(0, len(prices) + 1, 10))
    plt.xticks(rotation=30)
    plt.plot(dates, prices, label="Stock price")
    plt.scatter(buy_dates, prices)
    plt.vlines(x=buy_dates, ymin=40, ymax=110, colors='red', ls='--', lw=0.5, label='Buying')
    plt.vlines(x=sell_dates, ymin=40, ymax=110, colors='green', ls='--', lw=0.5, label='Selling')
    plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    main()