from datetime import datetime
import csv
import pandas as pd
class transaction:
    def __init__(self,amount,catagory, type,date:datetime, month, year):
        self.date = date
        self.get_amount(amount)
        self.get_type(type)
        self.catagory = catagory
        self.month = month
        self.year = year
    def get_amount(self,amount):
        if amount>0:
            self.amount = amount
        else:
            raise ValueError()
    def get_type(self,type):
        if not(type==1 or type==-1):
            raise ValueError()
        else:
            self.type =type
    def add_to_file(self, address):
        df = pd.read_csv(address)
        dictionary = {"id":1,"type": self.type, "amount": self.amount,"year":self.date.year, "month":self.date.month,"day":self.date.day}
        try:
            with open(address, "a") as file:
                row_count = sum(1 for _ in file)
                dictionary["id"]= row_count
                writer = csv.DictWriter(file, fieldnames=dictionary.keys())
                writer.writerow(dictionary)
        except FileNotFoundError:
            with open(address, "w") as file:
                writer = csv.DictWriter(file, fieldnames=dictionary.keys())
                writer.writeheader()
                writer.writerow(dictionary)
class investment:
    def __init__(self,stocks, bought_price):
        self.stocks = stocks
        self.bought_price = bought_price
        