import requests
import json
from datetime import date
class Investment:
    url = "https://fipiran.ir/services/fund/fundcompare"
    headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    date = None
    @classmethod
    def fetch(cls):
        if not cls.date or cls.date!= date.today():
            cls.date = date.today()
        else:
            return

        response = requests.post(cls.url, headers=headers, json={"key": "value"})
        data = response.json()
        with open("temp.json", "w") as f:
            json.dump(data,f,indent=4)
    @staticmethod
    def search_investment(name):
        data = json.load(open("temp.json", encoding="utf-8"))
        items = data["items"]
        matches = [item for item in items if name in item["name"]]
        return matches
    @staticmethod
    def find_price(investment:dict):
        return investment["cancelNav"]
