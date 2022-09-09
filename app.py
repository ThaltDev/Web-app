from flask import (Flask,request,render_template,redirect)
from data import *
import time
app=Flask(__name__)

@app.get("/home")
def home():

    return "form"

@app.get("/get_access")
def sent_mail():
    return render_template("acces.html")

linksCodes={}#codes:person

@app.post("/post/access")
def post_access():
    form=dict(request.form)
    data=promition.access(form["email"])
    if data:
        hashs=str(hash(str(time.time())+form["email"]))
        linksCodes.update({hashs:data[0]})
        email.sent.assec(form["email"],f"{request.url_root}link/home?code={hashs}&id={data[0]}")
        return "we sent you this email please check your email if you cann't see check and spam"
    return redirect("/home")

@app.post("/post/set_employe")
def set_employe_post():
    form=dict(request.form)
    print(sqlCode.employe.set_employe(form["email"],form["nameFirst"],form["nameLast"]))
    return redirect("/home")

@app.get("/link/home")
def LinkHome():
    args= dict(request.args)
    if "code" in args and "id" in args :
        if args["code"] in linksCodes and str(linksCodes[args["code"]])==str(args["id"]):
            return "have access stay in this link to have access"
    
    return redirect("/home")
@app.get("/set_employe")
def set_employe_get():
    return render_template("set_employe.html")
@app.get("/see_employes")
def page_employes():
    page = int(request.args["page"]) if "page" in request.args else 0
    data=sqlCode.employe.get_ten_employes(page*10)
    return render_template("see_employes.html",data=data[0],lenOfPage= data[1]//10 if data[1]/10==data[1]//10 else data[1]//10+1,position=page)
app.run()


