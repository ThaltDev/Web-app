from flask import (Flask,request,render_template,redirect,session,g,make_response)
from data import *
import time
import random
app=Flask(__name__)
app.secret_key="lalalalla"


def check_cookies(cookies):
    for i in cookies:
        if not i in session:
            return False
    return True

@app.get("/home")
def home():
    if 'code' in session and 'id' in session and (session['code'] in linksCodes and session['id']==linksCodes[str(session['code'])]):#static/img/images.jpg https://picsum.photos/500/300?random=1
        g.user=session['code']
        return render_template("mainEmployes.html")
    return "form"

@app.get("/get_access")
def sent_mail():
    return render_template("acces.html")

linksCodes={"0":"0"}#codes:person
@app.post("/post/access")
def post_access():
    form=dict(request.form)
    data=promition.access(form["email"])
    if data:
        hashs=str(hash(str(time.time())+form["email"]))
        linksCodes.update({hashs:str(data[0])})
        email.sent.assec(form["email"],f"{request.url_root}link/home?code={hashs}&id={data[0]}")
        return "we sent you this email please check your email if you cann't see check and spam"
    return redirect("/home")

@app.post("/post/set_employe")
def set_employe_post():
    form=dict(request.form)
    return redirect("/home")

@app.get("/link/home")
def LinkHome():
    args= dict(request.args)
    if "code" in args and "id" in args :
        if args["code"] in linksCodes and str(linksCodes[args["code"]])==str(args["id"]):
            session.pop('code',None)
            session.pop('id',None)
            session['code'] = str(args["code"])
            session['id'] = str(args["id"])
            return redirect("/home")
    
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

@app.route("/info/person",methods=["GET","POST"])
def info_personWithOutId():
    if request.method=="POST" and "id" in request.form:
        return redirect("/info/person/"+request.form["id"])
    return render_template("personWithOutId.html")

@app.get("/customers")
def costumers():
    page = int(request.args["page"]) if "page" in request.args else 0
    data=sqlCode.costumers.get_ten_customers(page*10)
    return render_template("customers.html",data=data[0],lenOfPage= data[1]//10 if data[1]/10==data[1]//10 else data[1]//10+1,position=page)

@app.route("/signup",methods=["post","get"])
def signup():
    if request.method=="POST":
        form= dict(request.form)
        if sqlCode.costumers.login(form['email'],form['name'],form["password"])==None:
            if sqlCode.costumers.singup(form['email'],form["name"],form['password']):
                return render_template("login.html",message="Now you can login")
        return render_template("signup.html",error="This username or email used")
    return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        form= dict(request.form)
        resoltues= sqlCode.costumers.login(form["email"],form['name'],form['password'])
        if resoltues:
            session.pop('username',None)
            session.pop('AssCode',None)
            session.pop("randomNumber",None)
            session.pop('password',None)
            session.pop('AssCode',None)
            session['username'] = sqlCode.costumers.getNameByEmail(form["email"]) if form['name']=='' else form["name"]
            session['randomNumber'] = str(random.randrange(-10000,10000))
            session['password']=sqlCode.costumers.getPrievityCode(form['password'])
            session['AssCode'] = sqlCode.costumers.getPrievityCode(session['password']+session['randomNumber'])
            return redirect("/home/customer")
        elif resoltues==None:
            message="This name or email doesn't used for any customer"
        else:
            message="Password is fault"
        return render_template("login.html",message=message)
    return render_template("login.html")

@app.get("/home/customer")
def customerHome():
    if check_cookies(["username","randomNumber","password","AssCode"]):
        if sqlCode.costumers.check(session['username'],session["randomNumber"],session["password"],session['AssCode']):
            return render_template("customerHome.html",username=session['username'])
        else:
            session.pop('username',None)
            session.pop('AssCode',None)
            session.pop("randomNumber",None)
            session.pop('password',None)
            session.pop('AssCode',None)
            return make_response("not found",503)
    else:
        return "For now you don't have access to see the product you need first <a href='/login'>log in</a> or <a href='/signup'>sign up</a>"

#i will append a print command when i run the procket to remder what i have done
if "see":
    print("http://localhost:5000/home for see if you have acces-login")
    print("http://localhost:5000/get_access for input your email can if you can get access with take a email with a link")
    print("http://localhost:5000/link/home is from the email you sent you")
    print("http://localhost:5000/set_employe for set a new employe you doesn't need to have acces")
    print("http://localhost:5000/see_employes for see employes can get args to see 10 specif employes from a page?=1 you get first 10 employes")
    print("http://localhost:5000/update_salary is for update salary from employe this need to have access")
    print("http://localhost:5000/info/person/<id> is for get info for employe but if you have accees")
    print("http://localhost:5000/customers for see customers like employe")
    print("http://localhost:5000/login for login customers")
    print("http://localhost:5000/signup fro sign up customers in this platfrom")
app.run(port=5000,debug=True)


