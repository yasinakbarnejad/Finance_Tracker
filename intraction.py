from datetime import datetime
import csv
class transaction:
    def __init__(self,amount,catagory, type):
        self.date = datetime.today()
        self.get_amount(amount)
        self.get_type(type)
        self.catagory = catagory
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
    def add_to_file(self,id, address):
        dictionary = {"id":id,"type": self.type, "amount": self.amount,"year":self.date.year, "month":self.date.month,"day":self.date.day}
        with open(address, "a") as file:
            writer = csv.DictWriter(file, fieldnames=dictionary.keys())
            writer.writerow(dictionary)
class investment:
    def __init__(self,stocks, bought_price):
        self.stocks = stocks
        self.bought_price = bought_price
        