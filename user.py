from datetime import date
from intraction import transaction
import pandas as pd
import json
class User:
    address = "data/users.json"
    def __init__(self, first_name, last_name,username, password,net_worth):
        self.first = first_name
        self.last = last_name
        self.username = username
        self.password = password
        self.net_worth = net_worth
        self.investments = []
        self.last_login = date.today()
        self.db_address = f"{self.last}_actions.csv"
    def add_investment(self, new_investment):
        self.investments.append(new_investment)
    def check_investments(self):
        new_list = []
        for investment in self.investments:
            if not investment.check_empty():
                new_list.append(investment)
        self.investments = new_list
    def calculate_investment(self):
        for investment in self.investments:
            investment.calculate()
    def action(self,new_action:transaction):
        self.net_worth += new_action.type*new_action.amount
        
    def login(self):
        self.calculate_investment()
        self.last_login = date.today()
    
    @classmethod
    def find_user(cls, username):
        try:
            with open(cls.address,"r") as f:
                users =  json.load(f)["users"]
        except FileNotFoundError:
            users = []
        if not users:
            return {}
        for user in users:
            if user["username"]==username:
                return User.read_dict(user) 
        else:
            return {} 
    @staticmethod
    def read_dict(user_dict):
        new_user = User(user_dict["first_name"],user_dict["last_name"],user_dict["username"],
                        user_dict["password"],user_dict["net_worth"])
        return new_user
    
    def add_file(self):
        new_user = {"first_name":self.first,"last_name":self.last,"username":self.username,
                    "password":self.password, "net_worth":self.net_worth}
        try:
            with open(User.address,"r") as f:
                old_dict = json.load(f)
                users = old_dict["users"]
        except FileNotFoundError:
            old_dict = {"users":[]}
            users = []
        
        users.append(new_user)
        old_dict["users"] = users
        with open(User.address, "w") as f:
            json.dump(old_dict,f, indent=4)
        
    def read_file(self):
        df = pd.read_csv(self.db_address)
        return df   
