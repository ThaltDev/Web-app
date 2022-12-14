import sqlite3 as sql
import hashlib
name="data.db"
if 1:
    import smtplib, ssl
    #import email
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    #MIMEText =email.mime.text.MIMEText
    #MIMEMultipart=email.mime.multipart.MIMEMultipart
    sender_email="thaltsek411@gmail.com"
    a=open("password.config")
    password =a.read()
    a.close()

class sqlCode():
    class employe():
        def get_ten_employes(position_start):
            employesList=[]
            connection = sql.connect(name,check_same_thread=False)
            fine2=0
            try:
                cursor = connection.cursor()
                employesList=cursor.execute(f"select id,FirstName,LastName from employes limit 10 offset {position_start}").fetchall()
                fine2=cursor.execute(f"select count(*) from employes").fetchone()[0]
            except:
                pass
            connection.commit()
            cursor.close()
            connection.close()
            return [employesList,fine2]
        def get_employe_by_id(id):
            employeInfo=[]
            more=[]
            connection = sql.connect(name,check_same_thread=False)
            try:
                cursor = connection.cursor()
                employeInfo=cursor.execute(f"select id,email,FirstName,LastName from employes where id={id}").fetchall()
                connection.commit()
                more=cursor.execute(f"select f.bonus,f.date_hire,f.fire_bool,(select d.perYear from salary as d where d.id=(select e.salary_id from bank as e where e.employe_id={id})) from bank as f where f.employe_id={id}").fetchall()
            except:
                pass
            connection.commit()
            cursor.close()
            connection.close()
            return {"basic":employeInfo,"excar":more}
        def set_employe(email,nameFirst,nameLast):
            connection = sql.connect(name,check_same_thread=False)
            try:
                cursor = connection.cursor()
                id = cursor.execute(f"select max(id) from bank;").fetchone()[0]+1
                connection.commit()

                id_2= cursor.execute(f"select max(id) from servies;").fetchone()[0]+1
                connection.commit()

                cursor.execute(f"insert into employes(email,nameFirst,nameLast,bank_id,servies_id)values('{email}','{nameFirst}','{nameLast}',{id},{id_2})")
                connection.commit()

                cursor.execute(f"insert into bank(date_hire,id)values(date(),{id})")            
                connection.commit()

                cursor.execute(f"insert into servies(employe_id,id)values((select id from employes where email='{email}'),{id_2})")            
                connection.commit()
            except:
                print("error to set employe")
                print(email,"\n",nameFirst,"\n",nameLast)
                pass
            connection.commit()
            cursor.close()
            connection.close()
        def update_salary(employ_id,salary):
            connection = sql.connect(name,check_same_thread=False)
            update_fine=False
            if 1:
                cursor = connection.cursor()
                salary_id=cursor.execute(f"select salary_id from bank where id=(select bank_id from employes where id={employ_id});").fetchone()[0]
                connection.commit()
                if cursor.execute(f"select max(id) from salary;").fetchone()[0]!=None:
                    id_max= cursor.execute(f"select max(id) from salary;").fetchone()[0]+1
                else:
                    id_max=1
                connection.commit()

                cursor.execute(f"update bank set salary_id={id_max} where id=(select bank_id from employes where id={employ_id}); ")
                connection.commit()
                if salary_id==None:
                    cursor.execute(f"insert into salary(perYear,id)values({salary},{id_max});")
                    connection.commit()
                else: #i think it better write update and the previous line get out of if and next line is update previous_salary_id 
                    cursor.execute(f"insert into salary(perYear,previous_salary_id,id)values({salary},{salary_id},{id_max});")
                    connection.commit()                    

                update_fine=True

            """except:
                print("error")
                pass"""
            connection.commit()
            cursor.close()
            connection.close()
            return update_fine
    class costumers():
        def howmanyUsersUsedNowServies():
            connection = sql.connect(name,check_same_thread=False)
            count=0
            try:
                cursor = connection.cursor()
                count=cursor.execute(f"select count(servies_help_now) from costumer").fetchone()
            except:
                pass
            connection.commit()
            cursor.close()
            connection.close()
            return count
        def howmanyUsedThisApp():
            connection = sql.connect(name,check_same_thread=False)
            count=0
            try:
                cursor = connection.cursor()
                count=cursor.execute(f"select count(time_used_app) from costumer").fetchone()
            except:
                pass
            connection.commit()
            cursor.close()
            connection.close()
            return count
        def count():
            connection = sql.connect(name,check_same_thread=False)
            count=0
            try:
                cursor = connection.cursor()
                count=cursor.execute(f"select count(*) from costumer").fetchone()
            except:
                pass
            connection.commit()
            cursor.close()
            connection.close()
            return count
        def get_ten_customers(position_start):
            employesList=[]
            connection = sql.connect(name,check_same_thread=False)
            fine2=0
            try:
                cursor = connection.cursor()
                employesList=cursor.execute(f"select id,name from customer limit 10 offset {position_start}").fetchall()
                fine2=cursor.execute(f"select count(*) from customer").fetchone()[0]
            except:
                pass
            connection.commit()
            cursor.close()
            connection.close()
            return [employesList,fine2]
        def login(email,Username,password):
            connection = sql.connect(name,check_same_thread=False)
            check=f"name='{Username}'"
            login=False#can't login because set wrong password
            if email!="":
                check = f"email='{email}'"
            if 1:
                cursor = connection.cursor()
                id=cursor.execute(f"select id from customer where {check};").fetchone()
                if id!=None:
                    login=cursor.execute(f"select password from customer where id={id[0]};").fetchone()[0]==password#if exist this customer and can login
                else:
                    login=None#if doesn't exist this customer 
            else:
                print("error")
                pass
            connection.commit()
            cursor.close()
            connection.close()
            return login 
        def singup(email,Username,password):
            connection = sql.connect(name,check_same_thread=False)
            signup=False
            try:
                cursor = connection.cursor()
                signup=not not cursor.execute(f"INSERT into customer(email,name,password)Values('{email}','{Username}','{password}')")
            except:
                pass
            connection.commit()
            cursor.close()
            connection.close()
            return signup 
        def getNameByEmail(email):
            connection = sql.connect(name,check_same_thread=False)
            username=False
            try:
                cursor = connection.cursor()
                username=cursor.execute(f"select name from customer where email='{email}';")
            except:
                pass
            connection.commit()
            cursor.close()
            connection.close()
            return username 
        def getPrievityCode(code):
            return hash_server(code)
        def check(username,randomNumber,password,AssCode):
            connection = sql.connect(name,check_same_thread=False)
            checkBool=False
            try:
                cursor = connection.cursor()
                passwordTake=cursor.execute(f"select password from customer where name='{username}';").fetchone()
                if passwordTake==None:
                    return False
                passwordTake=passwordTake[0]
                hashPassword =hash_server(passwordTake)
                if password!=hashPassword:
                    return False
                return AssCode==hash_server(hashPassword+randomNumber)
            except:
                print("new are")
                pass
            connection.commit()
            cursor.close()
            connection.close()
            return checkBool 
class promition():
    def access(email):
        connection = sql.connect(name,check_same_thread=False)
        try:
            cursor = connection.cursor()
            acces=cursor.execute(f"select employe_id from access where employe_id=(select employe_id from employes where email='{email}');").fetchall()[0]
        except:
            print("problem")
            acces=False
        connection.commit()
        cursor.close()
        connection.close()
        return acces
    def set_access(email,nameFirst,nameLast):
        connection = sql.connect(name,check_same_thread=False)
        fine=False
        try:
            cursor = connection.cursor()
            fine=cursor.execute(f"insert into access(employe_id)values(select id from employes where '{email}'=email and'{nameFirst}'=FirstName and '{nameLast}'=LastName);").fetchall()
        except:
            pass
        connection.commit()
        cursor.close()
        connection.close()
        return fine

class email():
    class sent():
        def assec(email1='thaltsek411@gmail.com',code=""):
            email.send(receiver=email1, subject='Acces', text=f'hello go there for get acces {code}')

    def send(text,receiver,subject,html=False):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver

        text = text
        if html:
            html = html
            part2 = MIMEText(html, "html")
            message.attach(part2)
        part1 = MIMEText(text, "plain")

        message.attach(part1)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver, message.as_string())

def hash_server(value : str):
    return hashlib.sha256(value.encode("UTF-8")).hexdigest()