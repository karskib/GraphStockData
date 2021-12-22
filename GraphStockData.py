import tkinter as tk
import pandas_datareader as pdr
import matplotlib.pyplot as plt
from tkcalendar import *


class Get_Stock(tk.Frame):

    def __init__(self):
        super().__init__()
        self.pack()
        self.setupUI()
        self.stock = ''
        self.startdate = ''
        self.enddate = ''
        self.startorend = ''

    def setupUI(self):

        self.frameforbuttons = tk.Frame(self)
        self.frameforbuttons.pack(side='top')

        self.information = tk.Label(self.frameforbuttons, text='Please select the ticker name')
        self.information.grid(row=0, column=0, columnspan=2)
        self.information.configure(anchor='center')

        self.ticker = tk.Entry(self.frameforbuttons, text='TICKER', bd=2, relief=tk.RAISED)
        self.ticker.grid(row=1, column=0, sticky='w')

        self.start = tk.Label(self.frameforbuttons, text='START DATE', bd=2, relief=tk.RAISED)
        self.start.grid(row=2, column=0, sticky='w')

        self.end = tk.Label(self.frameforbuttons, text='END DATE', bd=2, relief=tk.RAISED)
        self.end.grid(row=3, column=0, sticky='w')

        self.button2 = tk.Button(self.frameforbuttons, text='Graph', command=self.plot, relief=tk.RAISED)
        self.button2.grid(row=1, column=1, sticky='e')

        self.button3 = tk.Button(self.frameforbuttons, text='Get start\ndate', command=self.show_calendar_start)
        self.button3.grid(row=2, column=1, sticky='e')

        self.button4 = tk.Button(self.frameforbuttons, text='Get end\ndate', command=self.show_calendar_end)
        self.button4.grid(row=3, column=1, sticky='e')

        self.cb = tk.IntVar()
        self.check_b = tk.Checkbutton(self, text='Include Rolling avg?', variable=self.cb, onvalue=1, offvalue=0,
                                      relief=tk.SUNKEN)
        self.check_b.pack(side=tk.LEFT)

    def get_stock_data(self):
        stock_data = pdr.get_data_yahoo(self.ticker.get(), start=self.cal.get_date(), end=self.cal2.get_date())
        stock_data['Moving avg'] = stock_data['Adj Close'].rolling(7).mean()
        return stock_data

    def plot(self):
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 6))
        data = self.get_stock_data()[['Adj Close', 'Moving avg']]
        if self.cb.get() == 0:
            ax1.plot(data['Adj Close'])
        else:
            ax1.plot(data)
        ax1.plot()
        ax1.set_title('Price graph')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Price')

        returns = data['Adj Close'].pct_change()
        returns.hist()
        ax2.set_title('Distribution of returns')

        plt.tight_layout()
        plt.show()

    def show_calendar_start(self):
        self.startorend = 'START'
        print(self.startorend)
        if self.startorend == 'START':
            top = tk.Toplevel()
            self.cal = Calendar(top,
                                font="Arial 14", selectmode='day',
                                cursor="hand1", date_pattern='y-mm-dd')
            self.cal.pack(fill="both", expand=True)
            self.butt = tk.Button(top, text='Get Date', command=self.get_date)
            self.butt.pack()

    def get_date(self):
        if self.startorend == 'START':
            self.startdate = self.cal.get_date()
            self.start.configure(text=self.startdate)
            print(self.startdate)
        else:
            self.enddate = self.cal2.get_date()
            self.end.configure(text=self.enddate)
            print(self.enddate)

    def show_calendar_end(self):
        self.startorend = 'END'
        print(self.startorend)
        if self.startorend == 'END':
            top = tk.Toplevel()
            self.cal2 = Calendar(top,
                                 font="Arial 14", selectmode='day',
                                 cursor="hand1", date_pattern='y-mm-dd')
            self.cal2.pack(fill="both", expand=True)
            self.cal2.pack(fill="both", expand=True)
            self.butt2 = tk.Button(top, text='Get Date', command=self.get_date)
            self.butt2.pack()


if __name__ == '__main__':
    win = tk.Tk()
    Get_Stock()
    tk.mainloop()
