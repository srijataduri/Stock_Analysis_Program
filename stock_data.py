# Summary: This module contains the functions used by both console and GUI programs to manage stock data.


import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import csv
import time
from datetime import datetime
from utilities import clear_screen
from utilities import sortDailyData
from stock_class import Stock, DailyData

# Create the SQLite database
def create_database():
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    cur = conn.cursor()
    createStockTableCmd = """CREATE TABLE IF NOT EXISTS stocks (
                            symbol TEXT NOT NULL PRIMARY KEY,
                            name TEXT,
                            shares REAL
                        );"""
    createDailyDataTableCmd = """CREATE TABLE IF NOT EXISTS dailyData (
                                symbol TEXT NOT NULL,
                                date TEXT NOT NULL,
                                price REAL NOT NULL,
                                volume REAL NOT NULL,
                                PRIMARY KEY (symbol, date)
                        );"""   
    cur.execute(createStockTableCmd)
    cur.execute(createDailyDataTableCmd)

# Save stocks and daily data into database
def save_stock_data(stock_list):
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    cur = conn.cursor()
    insertStockCmd = """INSERT INTO stocks
                            (symbol, name, shares)
                            VALUES
                            (?, ?, ?); """
    insertDailyDataCmd = """INSERT INTO dailyData
                                    (symbol, date, price, volume)
                                    VALUES
                                    (?, ?, ?, ?);"""
    for stock in stock_list:
        insertValues = (stock.symbol, stock.name, stock.shares)
        try:
            cur.execute(insertStockCmd, insertValues)
            cur.execute("COMMIT;")
        except:
            pass
        for daily_data in stock.DataList: 
            insertValues = (stock.symbol,daily_data.date.strftime("%m/%d/%y"),daily_data.close,daily_data.volume)
            try:
                cur.execute(insertDailyDataCmd, insertValues)
                cur.execute("COMMIT;")
            except:
                pass
    
# Load stocks and daily data from database
def load_stock_data(stock_list):
    stock_list.clear()
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    stockCur = conn.cursor()
    stockSelectCmd = """SELECT symbol, name, shares
                    FROM stocks; """
    stockCur.execute(stockSelectCmd)
    stockRows = stockCur.fetchall()
    for row in stockRows:
        new_stock = Stock(row[0],row[1],row[2])
        dailyDataCur = conn.cursor()
        dailyDataCmd = """SELECT date, price, volume
                        FROM dailyData
                        WHERE symbol=?; """
        selectValue = (new_stock.symbol)
        dailyDataCur.execute(dailyDataCmd,(selectValue,))
        dailyDataRows = dailyDataCur.fetchall()
        for dailyRow in dailyDataRows:
            daily_data = DailyData(datetime.strptime(dailyRow[0],"%m/%d/%y"),float(dailyRow[1]),float(dailyRow[2]))
            new_stock.add_data(daily_data)
        stock_list.append(new_stock)
    sortDailyData(stock_list)

# Get stock price history from web using Web Scraping
def retrieve_stock_web(dateStart, dateEnd, stock_list):
    # Convert m/d/yy strings to Unix timestamps for Yahoo URL
    dateFrom = str(int(time.mktime(time.strptime(dateStart, "%m/%d/%y"))))
    dateTo   = str(int(time.mktime(time.strptime(dateEnd,   "%m/%d/%y"))))

    recordCount = 0

    for stock in stock_list:
        symbol = stock.symbol

        url = (
            "https://finance.yahoo.com/quote/" + symbol +
            "/history?period1=" + dateFrom +
            "&period2=" + dateTo +
            "&interval=1d&filter=history&frequency=1d"
        )

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # ⚠️ IMPORTANT: do NOT disable JavaScript – it may hide the data table
        # options.add_experimental_option(
        #     "prefs",
        #     {'profile.managed_default_content_settings.javascript': 2}
        # )

        driver = None
        try:
            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(60)
            driver.get(url)

            # Give the page a moment to render JS if needed
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, "html.parser")
        except Exception as e:
            raise RuntimeWarning("Chrome Driver Not Found") from e
        finally:
            if driver is not None:
                try:
                    driver.quit()
                except:
                    pass

        # Find the history table (be lenient on class)
        table = soup.find("table")
        if not table:
            print(f"No table found for {symbol}")
            continue

        rows = table.find_all("tr")

        for tr in rows:
            tds = tr.find_all("td")
            rowList = [td.get_text(strip=True) for td in tds]

            # Standard data rows have 7 columns
            if len(rowList) != 7:
                continue

            try:
                date_obj = datetime.strptime(rowList[0], "%b %d, %Y")
                close_price = float(rowList[5].replace(",", ""))
                volume = float(rowList[6].replace(",", ""))
            except Exception as parse_err:
                # Skip rows that don't parse cleanly
                print("Skipping row for", symbol, rowList, parse_err)
                continue

            daily_data = DailyData(date_obj, close_price, volume)
            stock.add_data(daily_data)
            recordCount += 1

        # Debug: see how many records we got for this stock
        print(symbol, "records loaded:", len(stock.DataList))

    return recordCount

# Get price and volume history from Yahoo! Finance using CSV import.
def import_stock_web_csv(stock_list,symbol,filename):
    for stock in stock_list:
            if stock.symbol == symbol:
                with open(filename, newline='') as stockdata:
                    datareader = csv.reader(stockdata,delimiter=',')
                    next(datareader)
                    for row in datareader:
                        daily_data = DailyData(datetime.strptime(row[0],"%Y-%m-%d"),float(row[4]),float(row[6]))
                        stock.add_data(daily_data)

def main():
    clear_screen()
    print("This module will handle data storage and retrieval.")

if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()