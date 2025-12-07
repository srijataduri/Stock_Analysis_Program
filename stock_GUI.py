# Summary: This module contains the user interface and logic for a graphical user interface version of the stock manager program.

from datetime import datetime
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import csv
import stock_data
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class StockApp:
    def __init__(self):
        self.stock_list = []
        #check for database, create if not exists
        if path.exists("stocks.db") == False:
            stock_data.create_database()

 # This section creates the user interface

        # Create Window
        self.root = Tk()
        self.root.title("Taduri's Stock Manager")

        # Build UI
        self.create_menus()
        self.create_widgets()

        # Add Menubar

        # Add File Menu


        # Add Web Menu 


        # Add Chart Menu
 

        # Add menus to window       


        # Add heading information

        

        # Add stock list

        
        
        # Add Tabs
 
        

        # Set Up Main Tab

        # Setup History Tab

        
        
        # Setup Report Tab


        ## Call MainLoop
        self.root.mainloop()

#implement UI methods
    def create_menus(self):
        # Create menubar
        self.menubar = Menu(self.root)

        # ----- File Menu -----
        file_menu = Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Load Data", command=self.load)
        file_menu.add_command(label="Save Data", command=self.save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=file_menu)

        # ----- Web Menu -----
        web_menu = Menu(self.menubar, tearoff=0)
        web_menu.add_command(label="Get Web Data", command=self.scrape_web_data)
        web_menu.add_command(label="Import CSV", command=self.importCSV_web_data)
        self.menubar.add_cascade(label="Web", menu=web_menu)

        # ----- Chart Menu -----
        chart_menu = Menu(self.menubar, tearoff=0)
        chart_menu.add_command(label="Display Chart", command=self.display_chart)
        self.menubar.add_cascade(label="Chart", menu=chart_menu)

        # Attach menubar to window
        self.root.config(menu=self.menubar)
    def create_widgets(self):
        # ----- Heading at top -----
        self.headingLabel = Label(
            self.root,
            text="No stock selected",
            font=("Helvetica", 14, "bold")
        )
        self.headingLabel.pack(pady=5)

        # ----- Tabs -----
        self.notebook = ttk.Notebook(self.root)
        self.main_tab = Frame(self.notebook)
        self.history_tab = Frame(self.notebook)
        self.report_tab = Frame(self.notebook)

        self.notebook.add(self.main_tab, text="Main")
        self.notebook.add(self.history_tab, text="History")
        self.notebook.add(self.report_tab, text="Report")
        self.notebook.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # =========================================
        # MAIN TAB  (stocks list + add/buy/sell)
        # =========================================

        # Left side: list of stocks
        left_frame = Frame(self.main_tab)
        left_frame.pack(side=LEFT, fill=Y, padx=5, pady=5)

        Label(left_frame, text="Stocks").pack()

        list_frame = Frame(left_frame)
        list_frame.pack(fill=BOTH, expand=True)

        self.stockList = Listbox(list_frame, height=15)
        self.stockList.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(list_frame, orient=VERTICAL, command=self.stockList.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.stockList.config(yscrollcommand=scrollbar.set)

        # When user selects a stock, update the other tabs
        self.stockList.bind("<<ListboxSelect>>", self.update_data)

        # Right side: add/update controls
        right_frame = Frame(self.main_tab)
        right_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=5)

        # ----- Add Stock section -----
        add_frame = LabelFrame(right_frame, text="Add Stock")
        add_frame.pack(fill=X, pady=5)

        Label(add_frame, text="Symbol:").grid(row=0, column=0, sticky=E, padx=2, pady=2)
        self.addSymbolEntry = Entry(add_frame, width=10)
        self.addSymbolEntry.grid(row=0, column=1, padx=2, pady=2)

        Label(add_frame, text="Name:").grid(row=1, column=0, sticky=E, padx=2, pady=2)
        self.addNameEntry = Entry(add_frame, width=25)
        self.addNameEntry.grid(row=1, column=1, padx=2, pady=2)

        Label(add_frame, text="Shares:").grid(row=2, column=0, sticky=E, padx=2, pady=2)
        self.addSharesEntry = Entry(add_frame, width=10)
        self.addSharesEntry.grid(row=2, column=1, padx=2, pady=2)

        Button(add_frame, text="Add Stock", command=self.add_stock).grid(
            row=3, column=0, columnspan=2, pady=5
        )

        # ----- Update Shares section -----
        update_frame = LabelFrame(right_frame, text="Update Shares")
        update_frame.pack(fill=X, pady=10)

        Label(update_frame, text="Shares:").grid(row=0, column=0, sticky=E, padx=2, pady=2)
        self.updateSharesEntry = Entry(update_frame, width=10)
        self.updateSharesEntry.grid(row=0, column=1, padx=2, pady=2)

        Button(update_frame, text="Buy", command=self.buy_shares).grid(
            row=1, column=0, padx=2, pady=5, sticky=E+W
        )
        Button(update_frame, text="Sell", command=self.sell_shares).grid(
            row=1, column=1, padx=2, pady=5, sticky=E+W
        )
        Button(update_frame, text="Delete Stock", command=self.delete_stock).grid(
            row=2, column=0, columnspan=2, padx=2, pady=5, sticky=E+W
        )

        # =========================================
        # HISTORY TAB  (daily price/volume)
        # =========================================
        self.dailyDataList = Text(self.history_tab, width=60, height=20)
        self.dailyDataList.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # =========================================
        # REPORT TAB  (summary info)
        # =========================================
        self.stockReport = Text(self.report_tab, width=60, height=20)
        self.stockReport.pack(fill=BOTH, expand=True, padx=5, pady=5)

# This section provides the functionality
       
    # Load stocks and history from database.
    def load(self):
        self.stockList.delete(0,END)
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list)
        for stock in self.stock_list:
            self.stockList.insert(END,stock.symbol)
        messagebox.showinfo("Load Data","Data Loaded")

    # Save stocks and history to database.
    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data","Data Saved")

    # Refresh history and report tabs
    def update_data(self, evt):
        self.display_stock_data()

    # Display stock price and volume history.
    def display_stock_data(self):
        # Make sure something is selected in the listbox
        selection = self.stockList.curselection()
        if not selection:
            return  # nothing selected; just do nothing

        index = selection[0]
        symbol = self.stockList.get(index)

        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
                self.dailyDataList.delete("1.0", END)
                self.stockReport.delete("1.0", END)
                self.dailyDataList.insert(END, "- Date -   - Price -   - Volume -\n")
                self.dailyDataList.insert(END, "=================================\n")
                for daily_data in stock.DataList:
                    row = (
                            daily_data.date.strftime("%m/%d/%y")
                            + "   "
                            + '${:0,.2f}'.format(daily_data.close)
                            + "   "
                            + str(daily_data.volume)
                            + "\n"
                    )
                    self.dailyDataList.insert(END, row)

                #display report


                    

    
    # Add new stock to track.
    def add_stock(self):
        new_stock = Stock(self.addSymbolEntry.get(),self.addNameEntry.get(),float(str(self.addSharesEntry.get())))
        self.stock_list.append(new_stock)
        self.stockList.insert(END,self.addSymbolEntry.get())
        self.addSymbolEntry.delete(0,END)
        self.addNameEntry.delete(0,END)
        self.addSharesEntry.delete(0,END)

    # Buy shares of stock.
    def buy_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.buy(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Buy Shares","Shares Purchased")
        self.updateSharesEntry.delete(0,END)

    # Sell shares of stock.
    def sell_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.sell(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Sell Shares","Shares Sold")
        self.updateSharesEntry.delete(0,END)

    # Remove stock and all history from being tracked.
    def delete_stock(self):
       pass

    # Get data from web scraping.
    def scrape_web_data(self):
        if not self.stock_list:
            messagebox.showinfo("No Stocks",
                                "Please add or load at least one stock before getting web data.")
        dateFrom = simpledialog.askstring("Starting Date","Enter Starting Date (m/d/yy)")
        dateTo = simpledialog.askstring("Ending Date","Enter Ending Date (m/d/yy")
        try:
            stock_data.retrieve_stock_web(dateFrom,dateTo,self.stock_list)
        except:
            messagebox.showerror("Cannot Get Data from Web","Check Path for Chrome Driver")
            return
        self.display_stock_data()
        messagebox.showinfo("Get Data From Web","Data Retrieved")

    # Import CSV stock history file.
    def importCSV_web_data(self):
        symbol = self.stockList.get(self.stockList.curselection())
        filename = filedialog.askopenfilename(title="Select " + symbol + " File to Import",filetypes=[('Yahoo Finance! CSV','*.csv')])
        if filename != "":
            stock_data.import_stock_web_csv(self.stock_list,symbol,filename)
            self.display_stock_data()
            messagebox.showinfo("Import Complete",symbol + "Import Complete")   
    
    # Display stock price chart.

    def display_chart(self):
        # Make sure something is selected
        selection = self.stockList.curselection()
        if not selection:
            messagebox.showinfo("No Stock Selected", "Please select a stock first.")
            return

        index = selection[0]
        symbol = self.stockList.get(index)

        # Optional: check if it has any data
        for stock in self.stock_list:
            if stock.symbol == symbol:
                if not stock.DataList:
                    messagebox.showinfo("No Data",
                                        f"No history data for {symbol}. Scrape or import first.")
                    return
                break

        # Call the utilities function that actually draws the chart
        display_stock_chart(self.stock_list, symbol)


def main():
        app = StockApp()
        

if __name__ == "__main__":
    # execute only if run as a script
    main()