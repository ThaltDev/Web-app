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
                employesList=cursor.execute(f"select id,nameFirst,nameLast from employes limit 10 offset {position_start}").fetchall()
                fine2=cursor.execute(f"select count(*) from employes").fetchone()[0]
            except:
                pass
            connection.commit()
            cursor.close()
            connection.close()
            return [employesList,fine2]
        def get_employe_by_id(id):
            employeInfo=[]
            connection = sql.connect(name,check_same_thread=False)
            try:
                cursor = connection.cursor()
                employeInfo=cursor.execute(f"select * from employes where id={id}").fetchone()
            except:
                pass
            connection.commit()
            cursor.close()
            connection.close()
            return employeInfo
        def set_employe(email,nameFirst,nameLast):
            connection = sql.connect(name,check_same_thread=False)
            try:
                cursor = connection.cursor()
                id = cursor.execute(f"select max(id) from salaries;").fetchone()[0]+1
                connection.commit()

                id_2= cursor.execute(f"select max(id) from servies;").fetchone()[0]+1
                connection.commit()

                cursor.execute(f"insert into employes(email,nameFirst,nameLast,salaries_id,servies_id)values('{email}','{nameFirst}','{nameLast}',{id},{id_2})")
                connection.commit()

                cursor.execute(f"insert into salaries(date_hire,id)values(date(),{id})")            
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
class promition():
    def access(email):
        connection = sql.connect(name,check_same_thread=False)
        try:
            cursor = connection.cursor()
            acces=cursor.execute(f"select nameFirst,nameLast,employe_id from access where email='{email}'").fetchall()[0]
        except:
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
            fine=cursor.execute(f"insert into access(email,nameFirst,nameLast,employe_id)values({email},{nameFirst},{nameLast},select email from employes where '{email}'=email);").fetchall()
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