from datetime import date
from intraction import transaction
import pandas as pd
class User:
    def __init__(self, first_name, last_name, password,net_worth):
        self.first = first_name
        self.last = last_name
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
    
    def read_file(self):
        df = pd.read_csv(self.db_address)
        return df   
