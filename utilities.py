#Helper Functions

import matplotlib.pyplot as plt
import os
import sys
from os import system, name

# Function to Clear the Screen
def clear_screen():
    if sys.stdout.isatty():
        os.system("clear")

# Function to sort the stock list (alphabetical)
def sortStocks(stock_list):
    ## Sort the stock list
    pass


# Function to sort the daily stock data (oldest to newest) for all stocks
def sortDailyData(stock_list):
    pass

# Function to create stock chart
# utilities.py
from datetime import datetime
import matplotlib.pyplot as plt

from stock_class import Stock, DailyData
from utilities import sortDailyData  # if sortDailyData is here; otherwise adjust import


def display_stock_chart(stock_list, symbol):
    # Find the stock
    target_stock = None
    for stock in stock_list:
        if stock.symbol == symbol:
            target_stock = stock
            break

    if target_stock is None:
        print(f"Stock {symbol} not found.")
        return

    if not target_stock.DataList:
        print(f"No data for {symbol}.")
        return

    # Sort data if necessary
    sortDailyData(target_stock.DataList)  # if your assignment wants them sorted by date

    dates = [d.date for d in target_stock.DataList]
    closes = [d.close for d in target_stock.DataList]

    # Plot
    plt.figure()
    plt.plot(dates, closes)
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.title(f"Price History for {symbol}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()