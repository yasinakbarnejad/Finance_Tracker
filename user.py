from datetime import date
from intraction import transaction
import json
import report
from investment import Investment
class User:
    address = "data/users.json"
    def __init__(self, first_name, last_name,username, password,net_worth):
        self.first = first_name
        self.last = last_name
        self.username = username
        self.password = password
        self.liquid = net_worth
        self.net_worth = self.liquid
        self.investments:list[Investment] = []
        self.last_login = date.today()
        self.db_address = f"data/trans/{self.username}_actions.csv"
        self.Icatagories = ["dad allowance", "mom gift", "salary"]
        self.Ecatagories = ["internet", "transportation"]
    def add_investment(self, new_investment:Investment):
        self.investments.append(new_investment)
    def check_investments(self):
        new_list = []
        for investment in self.investments:
            if not investment.is_empty():
                new_list.append(investment)
        self.investments = new_list
    def add_catagory(self, new_catagory, type):
        if type==1:
            self.Icatagories.append(new_catagory)
        else:
            self.Ecatagories.append(new_catagory)
    def action(self,new_action:transaction):
        self.net_worth += new_action.type*new_action.amount
        new_action.add_to_file(self.db_address)
        self.add_file()
    def login(self):
        self.last_login = date.today()
    @classmethod
    def find_user_dict(cls, username):
        try:
            with open(cls.address,"r") as f:
                users =  json.load(f)["users"]
        except FileNotFoundError:
            users = []
        if not users:
            return {}
        for user in users:
            if user["username"]==username:
                return user 
        else:
            return {} 
    @classmethod
    def find_user(cls, username):
        if user:=User.find_user_dict(username):
            return User.read_dict(user)
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
        if old_user :=self.find_user_dict(self.username):
            users.remove(old_user)
        users.append(new_user)
        old_dict["users"] = users
        with open(User.address, "w") as f:
            json.dump(old_dict,f, indent=4)
    def make_report(self, rtype, **kwrg):
        if rtype==1:
            return report.Monthly(address=self.db_address,**kwrg)
        elif rtype==2:
            return report.Annual(address=self.db_address,**kwrg)
        elif rtype==3:
            return report.Net(address=self.db_address,**kwrg)

