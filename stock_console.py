# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortDailyData
from os import path
import stock_data

# Main Menu
def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","5","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer ---")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve)")
            print("0 - Exit Program")
            option = input("Enter Menu Option: ")
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        else:
            clear_screen()
            print("Goodbye")

# Manage Stocks
def manage_stocks(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            option = input("Enter Menu Option: ")
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            delete_stock(stock_list)
        elif option == "4":
            list_stocks(stock_list)
        else:
            print("Returning to Main Menu")

# Add new stock to track
def add_stock(stock_list):
    clear_screen()
    print("Add Stock ---")
    symbol = input("Enter stock symbol (or 0 to cancel): ").strip().upper()
    if symbol == "0":
        return

    name = input("Enter company name: ").strip()
    shares_str = input("Enter number of shares: ")

    try:
        shares = float(shares_str)
    except ValueError:
        print("Invalid number for shares.")
        input("Press Enter to continue...")
        return

    # Create and add Stock object
    new_stock = Stock(symbol, name, shares)
    stock_list.append(new_stock)

    print(f"Stock {symbol} added with {shares} shares.")
    input("Press Enter to continue...")
        
# Buy or Sell Shares Menu
def update_shares(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Update Shares ---")
        print("1 - Buy Shares")
        print("2 - Sell Shares")
        print("0 - Return to Manage Stocks")
        option = input("Enter Menu Option: ")

        if option == "1":
            buy_stock(stock_list)
        elif option == "2":
            sell_stock(stock_list)
        elif option == "0":
            print("Returning to Manage Stocks...")
            input("Press Enter to continue...")
        else:
            print("*** Invalid Option - Try again ***")
            input("Press Enter to continue...")


# Buy Stocks (add to shares)
def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares ---")

    if not stock_list:
        print("No stocks in portfolio. Add stocks first.")
        input("Press Enter to continue...")
        return

    print("Stock List: [", end="")
    print(", ".join([s.symbol for s in stock_list]), end="]\n")

    symbol = input("Enter stock symbol: ").strip().upper()
    shares_str = input("Enter number of shares to BUY: ")

    try:
        shares = float(shares_str)
    except ValueError:
        print("Invalid number for shares.")
        input("Press Enter to continue...")
        return

    for stock in stock_list:
        if stock.symbol == symbol:
            stock.buy(shares)
            print(f"Bought {shares} shares of {symbol}. New total: {stock.shares}")
            input("Press Enter to continue...")
            return

    print(f"Symbol {symbol} not found in portfolio.")
    input("Press Enter to continue...")

# Sell Stocks (subtract from shares)
def sell_stock(stock_list):
    clear_screen()
    print("Sell Shares ---")

    if not stock_list:
        print("No stocks in portfolio. Add stocks first.")
        input("Press Enter to continue...")
        return

    print("Stock List: [", end="")
    print(", ".join([s.symbol for s in stock_list]), end="]\n")

    symbol = input("Enter stock symbol: ").strip().upper()
    shares_str = input("Enter number of shares to SELL: ")

    try:
        shares = float(shares_str)
    except ValueError:
        print("Invalid number for shares.")
        input("Press Enter to continue...")
        return

    for stock in stock_list:
        if stock.symbol == symbol:
            stock.sell(shares)
            print(f"Sold {shares} shares of {symbol}. New total: {stock.shares}")
            input("Press Enter to continue...")
            return

    print(f"Symbol {symbol} not found in portfolio.")
    input("Press Enter to continue...")

# Remove stock and all daily data
def delete_stock(stock_list):
    clear_screen()
    pass


# List stocks being tracked
def list_stocks(stock_list):
    clear_screen()
    print("List of Stocks ---")

    if not stock_list:
        print("No stocks in portfolio.")
    else:
        print(f"{'Symbol':<10}{'Name':<25}{'Shares':>10}")
        print("-" * 45)
        for stock in stock_list:
            print(f"{stock.symbol:<10}{stock.name:<25}{stock.shares:>10}")

    input("\nPress Enter to continue...")

# Add Daily Stock Data
def add_stock_data(stock_list):
    clear_screen()
    pass

# Display Report for All Stocks
def display_report(stock_list):
    clear_screen()
    print("Stock Report ---\n")

    if not stock_list:
        print("No stocks in portfolio.")
        input("\nPress Enter to continue...")
        return

    for stock in stock_list:
        print(f"{stock.symbol} - {stock.name} ({stock.shares} shares)")

        if not stock.DataList:
            print("  No history data for this stock.\n")
            continue

        # Sort daily data by date (oldest to newest)
        sortDailyData(stock.DataList)

        # Header for this stock's history
        print(f"{'Date':<12}{'Close':>12}{'Volume':>15}")
        print("-" * 39)

        for day in stock.DataList:
            date_str = day.date.strftime("%m/%d/%y")
            close_str = f"{day.close:0.2f}"
            vol_str = f"{int(day.volume):,}"
            print(f"{date_str:<12}{close_str:>12}{vol_str:>15}")

        print()  # blank line between stocks

    input("Press Enter to continue...")


  


# Display Chart
def display_chart(stock_list):
    clear_screen()
    print("Display Chart ---")

    if not stock_list:
        print("No stocks in portfolio. Add stocks first.")
        input("Press Enter to continue...")
        return

    # Show available symbols
    print("Stock List: [", end="")
    print(", ".join([stock.symbol for stock in stock_list]), end="]\n")

    symbol = input("Enter stock symbol to display chart for: ").strip().upper()

    # Verify symbol exists
    if not any(stock.symbol == symbol for stock in stock_list):
        print(f"Symbol {symbol} not found in portfolio.")
        input("Press Enter to continue...")
        return

    # Optional: check if there is data for this stock
    has_data = False
    for stock in stock_list:
        if stock.symbol == symbol and stock.DataList:
            has_data = True
            break

    if not has_data:
        print(f"No history data for {symbol}. Scrape or import data first.")
        input("Press Enter to continue...")
        return

    # Call the shared chart function from utilities.py
    display_stock_chart(stock_list, symbol)

    # After the chart window is closed
    input("Press Enter to continue...")

# Manage Data Menu
def manage_data(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Data ---")
        print("1 - Save to Database")
        print("2 - Load from Database")
        print("3 - Retrieve Data from Web")
        print("4 - Import from CSV File")
        print("0 - Return to Main Menu")
        option = input("Enter Menu Option: ")

        if option == "1":
            clear_screen()
            stock_data.save_stock_data(stock_list)
            print("Data saved to database.")
            input("Press Enter to continue...")
        elif option == "2":
            clear_screen()
            stock_list.clear()
            stock_data.load_stock_data(stock_list)
            print("Data loaded from database.")
            input("Press Enter to continue...")
        elif option == "3":
            retrieve_from_web(stock_list)
        elif option == "4":
            import_csv(stock_list)
        elif option == "0":
            print("Returning to Main Menu...")
            input("Press Enter to continue...")
        else:
            print("*** Invalid Option - Try again ***")
            input("Press Enter to continue...")


# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    clear_screen()
    print("Retrieve Data From Web ---")

    if not stock_list:
        print("No stocks in portfolio. Add stocks first.")
        input("Press Enter to continue...")
        return

    date_start = input("Enter Starting Date (m/d/yy): ")
    date_end = input("Enter Ending Date (m/d/yy): ")

    try:
        records = stock_data.retrieve_stock_web(date_start, date_end, stock_list)
    except RuntimeWarning as e:
        print("Error retrieving data from web:", e)
        print("Check your ChromeDriver path or setup.")
        input("Press Enter to continue...")
        return
    except Exception as e:
        print("Unexpected error while retrieving data:", e)
        input("Press Enter to continue...")
        return

    print(f"Data retrieved successfully. Records loaded: {records}")
    input("Press Enter to continue...")
# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen()
    print("Import Data From CSV ---")

    if not stock_list:
        print("No stocks in portfolio. Add stocks first.")
        input("Press Enter to continue...")
        return

    print("Current Stocks: [", end="")
    print(", ".join([stock.symbol for stock in stock_list]), end="]\n")

    symbol = input("Enter stock symbol to import data for: ").strip().upper()

    if not any(stock.symbol == symbol for stock in stock_list):
        print(f"Symbol {symbol} not found in portfolio.")
        input("Press Enter to continue...")
        return

    filename = input("Enter CSV filename with full path: ").strip()

    if filename == "":
        print("No filename entered. Import cancelled.")
        input("Press Enter to continue...")
        return

    try:
        stock_data.import_stock_web_csv(stock_list, symbol, filename)
    except FileNotFoundError:
        print("File not found. Check the path and try again.")
        input("Press Enter to continue...")
        return
    except Exception as e:
        print("Error importing CSV:", e)
        input("Press Enter to continue...")
        return

    print(f"Import complete for {symbol}.")
    input("Press Enter to continue...")
# Begin program
def main():
    #check for database, create if not exists
    if path.exists("stocks.db") == False:
        stock_data.create_database()
    stock_list = []
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()