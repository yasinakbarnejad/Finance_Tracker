import requests
import json
from datetime import date
class Investment:

    date = None
    def __init__(self,name,stocks=0,bought=False,value=0,spent=0,):
        self.stocks = stocks
        self.bought = bought
        self.value = value
        self.spent = spent
        self.name = name
        self.price = 0
    def buy(self,stock, price):
        self.stocks += stock
        self.bought = True
        self.spent+= price * stock
        self.price = price
        self.calculate()
    def sell(self,stock,price):
        self.stocks -= stock
        if self.stocks==0:
            self.bought=False
        self.price = price
        self.calculate()
    def calculate(self):
        if self.price:
            self.value = self.stocks*self.price
            return  self.value - self.spent 
        else:
            return 0
    def is_empty(self):
        if self.stocks==0:
            return True
        else:
            return False
    @classmethod
    def fetch(cls):
        url = "https://fipiran.ir/services/fund/fundcompare"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if not cls.date or cls.date!= date.today():
            cls.date = date.today()
        else:
            return

        response = requests.post(url, headers=headers, json={"key": "value"})
        data = response.json()
        if response.status_code !=200:
            return
        with open("data/investment.json", "w") as f:
            json.dump(data,f,indent=4)
    @staticmethod
    def search_investment(name):
        data = json.load(open("temp.json", encoding="utf-8"))
        items = data["items"]
        matches = [item for item in items if name in item["name"]]
        return matches
    def find_price(self,price):
        self.price = round(price,1)
    def to_dict(self):
        return {"price":self.price,"name":self.name,"value":self.value,"spent":self.spent,
                "stocks":self.stocks,"bought":self.bought}
    @staticmethod
    def read_dict(new_dict):
        return Investment(new_dict["name"],new_dict["stocks"],new_dict["bought"],new_dict["value"],
                          new_dict["spent"])
