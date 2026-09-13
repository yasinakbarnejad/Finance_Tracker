import plotly.express as px
import pandas as pd
from datetime import date as dt
class Report:
    @staticmethod
    def read_file(address):
        return pd.read_csv(address)
class Monthly(Report):
    def __init__(self, month, address):
        df = self.read_file(address)
        self.first = self.compare_chart(df, month)
        self.second = self.expense_pie(df, month)
        self.third = self.income_pie(df, month)

    @staticmethod
    def compare_chart(df:pd.DataFrame, month):
        filtered_income = df[(df["type"]==1) & (df["month"]==month)]
        filtered_expense = df[(df["type"]==-1) & (df["month"]==month)] 
        income = filtered_income["amount"].sum()
        expense = filtered_expense["amount"].sum()
        df = pd.DataFrame({
            "label" : ["income", "expense"],
            "value" : [income, expense]
        })
        fig = px.histogram(
            df,
            x='label',
            y='value',
            color_discrete_map={'label': 'green', 'value': 'red'},
        )
        return fig
    @staticmethod
    def expense_pie(df:pd.DataFrame, month):
        filtered = df[(df["type"]==-1) & (df["month"]==month)] 
        final = filtered[["catagory","amount"]]
        df_grouped = final.groupby('catagory', as_index=False)['amount'].sum()
        return px.pie(df_grouped, values='amount', names='catagory')
    @staticmethod
    def income_pie(df:pd.DataFrame, month):
        filtered = df[(df["type"]==1) & (df["month"]==month)] 
        final = filtered[["catagory","amount"]]
        df_grouped = final.groupby('catagory', as_index=False)['amount'].sum()
        return px.pie(df_grouped, values='amount', names='catagory')
class Annual(Report):
    def __init__(self, year, address):
        df = self.read_file(address)
        self.first = self.compare_chart(df, year)
        self.second = self.expense_pie(df, year)
        self.third = self.income_pie(df, year)
    @staticmethod
    def income_pie(df:pd.DataFrame, year):
        filtered = df[(df["type"]==1) & (df["year"]==year)] 
        final = filtered[["catagory","amount"]]
        df_grouped = final.groupby('catagory', as_index=False)['amount'].sum()
        return px.pie(df_grouped, values='amount', names='catagory')
    @staticmethod
    def expense_pie(df:pd.DataFrame, year):
            filtered = df[(df["type"]==-1) & (df["year"]==year)] 
            final = filtered[["catagory","amount"]]
            df_grouped = final.groupby('catagory', as_index=False)['amount'].sum()
            return px.pie(df_grouped, values='amount', names='catagory')
    @staticmethod
    def compare_chart(df:pd.DataFrame, year):
        filtered_income = df[(df["type"]==1) & (df["year"]==year)]
        filtered_expense = df[(df["type"]==-1) & (df["year"]==year)] 
        income = filtered_income["amount"].sum()
        expense = filtered_expense["amount"].sum()
        df = pd.DataFrame({
            "label" : ["income", "expense"],
            "value" : [income, expense]
        })
        fig = px.histogram(
            df,
            x='label',
            y='value',
            color_discrete_map={'label': 'green', 'value': 'red'},
        )
        return fig
class Net(Report):
    def __init__(self,address, date,net_worth):
        df = self.read_file(address)
        df = df[df["date"]>=str(date)]
        df = df.assign(change= -df["amount"] *df["type"])
        df = pd.DataFrame(df.groupby(["date"],as_index=False)["change"].sum())

        df = df.sort_values(by=["date"],ascending=False)

        df["net"] = df["change"].cumsum()+net_worth
        df = df[["net","date"]]
        newrow = {"date" : str(dt.today()), "net": net_worth}
        df = pd.concat([pd.DataFrame([newrow]),df],ignore_index=False)
        self.first = px.line(df,x="date",y="net")

        
        