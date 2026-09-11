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
        dictionary = {"date":1 ,"type": self.type, "amount": self.amount,"year":self.year, "month":self.month,"date":self.date, "catagory": self.catagory}
        try:
            with open(address,"r",newline='') as file:
                row_count = sum(1 for _ in file)
                dictionary["id"]= row_count
        except FileNotFoundError:
            dictionary["id"]= 0
        with open(address, "a",newline='') as file:
            writer = csv.DictWriter(file, fieldnames=dictionary.keys())
            if dictionary["id"]==0:
                writer.writeheader()
            writer.writerow(dictionary)
class investment:
    def __init__(self,stocks, bought_price):
        self.stocks = stocks
        self.bought_price = bought_price
        