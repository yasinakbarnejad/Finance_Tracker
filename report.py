import plotly.express as px
import pandas as pd

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
            x='type',
            y='Toman',
            color_discrete_map={'income': 'green', 'expense': 'red'},
        )
        return fig
    @staticmethod
    def expense_pie(df:pd.DataFrame, month):
        filtered = df[(df["type"]==-1) & (df["month"]==month)] 
        final = filtered[["catagory","amount"]]
        df_grouped = final.groupby('catagory', as_index=False)['amount'].sum()
        return px.pie(df_grouped, values='expense', names='catagory')
    @staticmethod
    def income_pie(df:pd.DataFrame, month):
        filtered = df[(df["type"]==1) & (df["month"]==month)] 
        final = filtered[["catagory","amount"]]
        df_grouped = final.groupby('catagory', as_index=False)['amount'].sum()
        return px.pie(df_grouped, values='income', names='catagory')