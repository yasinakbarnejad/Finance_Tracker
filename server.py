import fastapi
from datetime import datetime
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse 
import uvicorn
from user import User
from intraction import investment, transaction
from fastapi.staticfiles import StaticFiles
import jdatetime

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
    
@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: fastapi.Request, error: str | None = None):
    return fronts.TemplateResponse(
        request,"signup.html", {"user": None, "error": error}
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


@app.post("/income")
def income(request:fastapi.Request,
          amount: int = fastapi.Form(...),
          catagory: str = fastapi.Form(...),
          date: str = fastapi.Form(...)):
    
    year, month, day = map(int, date.split("/"))
    jalali_date = jdatetime.date(year, month, day)
    gregorian_date = jalali_date.togregorian()
    
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
    jalali_date = jdatetime.date(year, month, day)
    gregorian_date = jalali_date.togregorian()
    
    try:
        new_trans = transaction(amount, catagory,-1, gregorian_date)
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
        print("not found")
        return fronts.TemplateResponse(request,"login.html", {"request":request, "error":"user is not found"})
    if user.password != password:
        print("wrong pass")
        return fronts.TemplateResponse(request,"login.html", {"request":request, "error":"password is wrong"})
    global main_user
    main_user = user
    return RedirectResponse("/home", status_code=303)

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

