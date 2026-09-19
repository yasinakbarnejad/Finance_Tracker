import jdatetime
import json
def date_convertor(jdate):
    year, month, day = map(int, jdate.split("/"))
    jalali_date = jdatetime.date(year, month, day)
    return jalali_date.togregorian()
def get_jdate():
    return  jdatetime.date.today().month, jdatetime.date.today().year
def get_names():
    with open("temp.json", "r") as file:
        name_dict = json.load(file)
    investments = name_dict["items"]
    names = [item["name"] for item in investments]
    name_dict = {"names" : names}
    with open("data/names.json","w") as file:
        json.dump(name_dict, file, indent=2)
