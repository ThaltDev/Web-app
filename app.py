from flask import (Flask,request,render_template,redirect,session,g,make_response)
from data import *
import time
app=Flask(__name__)
app.secret_key="lalalalla"
@app.get("/home")
def home():
    if 'code' in session and 'id' in session and (session['code'] in linksCodes and session['id']==linksCodes[str(session['code'])]):#static/img/images.jpg https://picsum.photos/500/300?random=1
        g.user=session['code']
        return "you have access"
    return "form"

@app.get("/get_access")
def sent_mail():
    return render_template("acces.html")

linksCodes={"0":"0"}#codes:person
@app.get("/test")
def test(access1=False):
    return f"<h1>{access1}</h1>"
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
            session.pop('code',None)
            session.pop('id',None)
            session['code'] = args["code"]
            session['id'] = args["id"]
            return "asd"
    
    return redirect("/home")
@app.get("/set_employe")
def set_employe_get():
    return render_template("set_employe.html")
@app.get("/see_employes")
def page_employes():
    page = int(request.args["page"]) if "page" in request.args else 0
    data=sqlCode.employe.get_ten_employes(page*10)
    return render_template("see_employes.html",data=data[0],lenOfPage= data[1]//10 if data[1]/10==data[1]//10 else data[1]//10+1,position=page)
@app.get("/update_salary")
def update_salary():
    return render_template("update_salary.html")
@app.post("/post/update_salary_by_id")
def post_update_salary_by_id():
    form = dict(request.form)
    if not ("id" in form and "salary" in form ):
        return make_response("404",404)
    if 'code' in session and 'id' in session and (session['code'] in linksCodes and session['id']==linksCodes[str(session['code'])]):
        sqlCode.employe.update_salary(form["id"],form["salary"])
        return render_template("person.html",info=sqlCode.employe.get_employe_by_id(form["id"]))
    else:
        return make_response("you haven't take access to do this",404)
@app.get("/info/person/<id>")
def get_person(id):
    if 'code' in session and 'id' in session and (session['code'] in linksCodes and session['id']==linksCodes[str(session['code'])]):
        return render_template("person.html",info=sqlCode.employe.get_employe_by_id(id))
    else:
        return make_response("you haven't take access to do this",404)

app.run()


