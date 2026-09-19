import fastapi
from datetime import datetime
import datetime
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse , JSONResponse
import uvicorn
from fastapi.encoders import jsonable_encoder
from user import User
from intraction import transaction
from fastapi.staticfiles import StaticFiles
import util
from investment import Investment

fronts = Jinja2Templates(directory="fronts")
app = fastapi.FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

main_user = None
@app.get("/" , response_class=HTMLResponse)
def home(request: fastapi.Request):
    return fronts.TemplateResponse(request,"main.html",
    {
        "response" : "success"
    })
@app.get("/home")
def main(request: fastapi.Request):
    return fronts.TemplateResponse(request,"main.html",
    {
        "request" : request,
        "user" : main_user
    })

@app.get("/contact", response_class=HTMLResponse)
def contact_page(request: fastapi.Request, error: str | None = None):
    return fronts.TemplateResponse(request,"contactus.html",
    {
        "request" : request,
        "user" : main_user
    })
@app.get("/report", response_class=HTMLResponse)
def report_page(request: fastapi.Request, error: str | None = None):
    return fronts.TemplateResponse(request,"report.html",
    {
        "request" : request,
        "user" : main_user,
        "type" : 0
    })
@app.get("/login", response_class=HTMLResponse)
def login_page(request: fastapi.Request, error: str | None = None):
    return fronts.TemplateResponse(
        request,"login.html", {"user": None, "error": error}
    )
@app.get("/investment", response_class=HTMLResponse)
def investment_page(request: fastapi.Request, error: str | None = None):
    return fronts.TemplateResponse(
        request,"investment.html", {"request":request,"user": main_user,"error":error}
    )  
@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: fastapi.Request, error: str | None = None):
    return fronts.TemplateResponse(
        request,"signup.html", {"user": None, "error": error}
    )
@app.get("/setting", response_class=HTMLResponse)
def setting_page(request: fastapi.Request, error: str | None = None):
    return fronts.TemplateResponse(
        request,"setting.html", {"user": main_user, "error": error}
    )
@app.post("/select", response_class=HTMLResponse)
def select_report_type(
    request:fastapi.Request,
    type: str= fastapi.Form(...)):
    if not type:
        type_num = 0 
    else:
        type_num = int(type)
    return fronts.TemplateResponse(request,"report.html", {"request":request, "user":main_user, "type" : type_num})
@app.post("/investment/investments", response_class=HTMLResponse)
def search(
    request: fastapi.Request,
    investment: str = fastapi.Form(...)
):
    Investment.fetch()
    limit = 10
    matches = Investment.search_investment(investment)

    if len(matches)>limit:
        return fronts.TemplateResponse(request,"investment.html", {
            "request":request,
            "user":main_user,
            "error":"Please be more specific",
            "investments":[]
            })
    resualt = []
    for investment_block in matches:
        bought= next((invest for invest in main_user.investments if investment_block["name"]==invest.name),None)
        if bought==None:
            bought = Investment(investment_block["name"])
        print(type(investment_block))
        bought.find_price(investment_block.get("cancelNav",-1))
        resualt.append(bought)
    print(resualt)
    return  fronts.TemplateResponse(request,"investment.html", {
                "request":request,
                "user":main_user,
                "error": "",
                "investments":resualt
                })
@app.post("/save")
def save(request:fastapi.Request,
          ctype: int = fastapi.Form(...),
          catagory: str = fastapi.Form(...)):
    main_user.add_catagory(catagory,ctype)
@app.post("/trade")
def trade(request:fastapi.Request,
          amount: int = fastapi.Form(...),
          name: str = fastapi.Form(...),
          action: int = fastapi.Form(...)):
    investment = next((item for item in main_user.investments if item.name==name),None)
    if investment:
        investment.buy(amount,investment.price)
    else:
        investment = Investment(name)
        matches = Investment.search_investment(name)
        investment_block = matches[0]
        investment.buy(amount,investment_block.get("cancelNav",-1))
        main_user.investments.append(investment)
    new_trans = transaction(amount, "investment",action, datetime.date.today(), *util.get_jdate())
    main_user.action(new_trans)
    return fronts.TemplateResponse(
        request,"setting.html", {"user": main_user, "error": error}
    )   
@app.post("/income")
def income(request:fastapi.Request,
          amount: int = fastapi.Form(...),
          catagory: str = fastapi.Form(...),
          date: str = fastapi.Form(...)):
    
    year, month, day = map(int, date.split("/"))
    gregorian_date = util.date_convertor(date)
    
    try:
        new_trans = transaction(amount, catagory,1, gregorian_date, month,year)
    except Exception as e:
        return fronts.TemplateResponse(request,"main.html", {"request":request, "error":repr(e)})
    if not main_user:
        return fronts.TemplateResponse(request,"main.html", {"request":request, "error": "no users logged in"})
    main_user.action(new_trans)
    return fronts.TemplateResponse(request,"main.html", {"request":request, "user":main_user})
@app.post("/expense")
def expense(request:fastapi.Request,
          amount: int = fastapi.Form(...),
          catagory: str = fastapi.Form(...),
          date: str = fastapi.Form(...)):
    
    year, month, day = map(int, date.split("/"))
    gregorian_date = util.date_convertor(date)
    
    try:
        new_trans = transaction(amount, catagory,-1, gregorian_date, month, year)
    except Exception as e:
        return fronts.TemplateResponse(request,"main.html", {"request":request, "error":repr(e)})
    if not main_user:
        return fronts.TemplateResponse(request,"main.html", {"request":request, "error": "no users logged in"})
    main_user.action(new_trans)
    return fronts.TemplateResponse(request,"main.html", {"request":request, "user":main_user})
@app.post("/login")
def login(request:fastapi.Request,
          username: str = fastapi.Form(...),
          password: str = fastapi.Form(...)):
    if (not username or not password):
        return fronts.TemplateResponse(request,"login.html", {"request":request, "error":"invalid input"})
    user = User.find_user(username)
    if not user:
        return fronts.TemplateResponse(request,"login.html", {"request":request, "error":"user is not found"})
    if user.password != password:
        return fronts.TemplateResponse(request,"login.html", {"request":request, "error":"password is wrong"})
    global main_user
    main_user = user
    return RedirectResponse("/home", status_code=303)
@app.post("/api/monthlychart")
def get_monthly_chart(request:fastapi.Request,
          months: str = fastapi.Form(...)):
    month_num= int(months)
    if not main_user:
            return fronts.TemplateResponse(request,"main.html", {"request":request, "error": "no users logged in"})
    report = main_user.make_report(1,month=month_num)
    return fronts.TemplateResponse(
    request,
    "report.html",
    {
        "request": request,
        "chart1": report.first.to_html(
            full_html=False,
            include_plotlyjs=True
        ),
        "chart2": report.second.to_html(
            full_html=False,
            include_plotlyjs=True
        ),
        "chart3": report.third.to_html(
            full_html=False,
            include_plotlyjs=True
        ),
        "user": main_user
    }
)
@app.post("/api/annualchart")
def get_monthly_chart(request:fastapi.Request,
          year: str = fastapi.Form(...)):
    year_num= int(year)
    if not main_user:
            return fronts.TemplateResponse(request,"main.html", {"request":request, "error": "no users logged in"})
    report = main_user.make_report(2,year=year_num)
    return fronts.TemplateResponse(
    request,
    "report.html",
    {
        "request": request,
        "chart1": report.first.to_html(
            full_html=False,
            include_plotlyjs=True
        ),
        "chart2": report.second.to_html(
            full_html=False,
            include_plotlyjs=True
        ),
        "chart3": report.third.to_html(
            full_html=False,
            include_plotlyjs=True
        ),
        "user": main_user
    }
)
@app.post("/api/netchart")
def get_monthly_chart(request:fastapi.Request,
          date: str = fastapi.Form(...)):
    if not main_user:
            return fronts.TemplateResponse(request,"main.html", {"request":request, "error": "no users logged in"})
    gdate = util.date_convertor(date)
    report = main_user.make_report(3,date=gdate,net_worth=main_user.net_worth)
    return fronts.TemplateResponse(
    request,
    "report.html",
    {
        "request": request,
        "chart1": report.first.to_html(
            full_html=False,
            include_plotlyjs=True
        ),
        "user":main_user
    }
)
@app.post("/signup")
def signup(request:fastapi.Request,
          fname: str = fastapi.Form(...),
          sname: str = fastapi.Form(...),
          username: str = fastapi.Form(...),
          repassword: str = fastapi.Form(...),
          password: str = fastapi.Form(...),
          net_worth: int = fastapi.Form(...)):
    if (net_worth < 0):
        return fronts.TemplateResponse(request,"signup.html", {"request":request, "error":"your net worth cant be negative"})
    user = User.find_user(username)
    if user:
        return fronts.TemplateResponse(request,"signup.html", {"request":request, "error":"user already exists"})
    if password != repassword:
        return fronts.TemplateResponse(request,"signup.html", {"request":request, "error":"passwords dont match"})
    
    global main_user
    main_user = User(fname,sname,username,password,net_worth)
    main_user.add_file()
    return RedirectResponse("/home", status_code=303)

