from flask import Flask,request,redirect,render_template,url_for,flash,session
from flask_mysqldb import MySQL
from flask_session import Session
from otp import genotp
from cmail import sendmail
from datetime import datetime
from datetime import date
import random
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from tokenreset import token
from io import BytesIO  
app=Flask(__name__)
app.secret_key='harpuj@7j'
app.config['SESSION_TYPE']='filesystem'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Admin'
app.config['MYSQL_DB']='hostel'
Session(app)
mysql=MySQL(app)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/About')
def About():
    return render_template('About.html')
@app.route('/MessMenu')
def MessMenu():
    return render_template('MessMenu.html')
@app.route('/AdminRegister',methods=['GET','POST'])
def AdminRegister():
    if request.method=='POST':
        Userid=request.form['Userid']
        email=request.form['email']
        password=request.form['password']
        conformpassword=request.form['conformpassword']
        cursor=mysql.connection.cursor()
        cursor.execute('Select Userid from admin')
        data=cursor.fetchall()
        cursor.execute('SELECT email from admin')
        edata=cursor.fetchall()
        if(email,) in edata:
            flash('Email id already already exists')
            return render_template('AdminRegister.html')
        cursor.close()
        otp=genotp()
        subject='Thanks for registering to the application'
        body=f'use this otp to register {otp}'
        sendmail(email,subject,body)
        return render_template('otp.html',otp=otp,Userid=Userid,email=email,password=password,conformpassword=conformpassword)
    else:
        flash('invalid email')
        return render_template('AdminRegister.html')
    return render_template('AdminRegister.html')
@app.route('/Adminlogin',methods=['GET','POST'])
def Adminlogin():
    if session.get('User'):
        return redirect(url_for('index'))
    if request.method=='POST':
        Userid=request.form['Userid']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('select count(*) from admin where Userid=%s and password=%s',[Userid,password])
        count=cursor.fetchone() [0]
        if count==0:
            flash('Invalid Userid or password')
            return render_template('Adminlogin.html')
        else:
            session['User']=Userid
            return redirect(url_for('index'))
    return render_template('Adminlogin.html')
@app.route('/index')
def index():
    if session.get('User'):
        return render_template('index.html')
    else:
        #implement flash
        flash('login first')
        return redirect(url_for('Adminlogin'))
@app.route('/logout')
def logout():
    if session.get('User'):
        session.pop('User')
        return redirect(url_for('home'))
    else:
        flash('already logged out!')
        return redirect(url_for('Adminlogin'))
@app.route('/otp/<otp>/<Userid>/<email>/<password>/<conformpassword>',methods=['GET','POST'])
def otp(otp,Userid,email,password,conformpassword):
    if request.method=='POST':
        uotp=request.form['otp']
        if otp==uotp:
            cursor=mysql.connection.cursor()
            lst=[Userid,email,password,conformpassword]
            query='insert into admin values(%s,%s,%s,%s)'
            cursor.execute(query,lst)
            mysql.connection.commit()
            cursor.close()
            flash('Details registered')
            return render_template('index.html')
        else:
            flash('Wrong otp')
            return render_template('otp.html',otp=otp,Userid=Userid,email=email,password=password,conformpassword=conformpassword)
@app.route('/forgotpassword',methods=['GET','POST'])
def forgotpassword():
    if request.method=='POST':
        Userid=request.form['Userid']
        cursor=mysql.connection.cursor()
        cursor.execute('select Userid from admin')
        data=cursor.fetchall()
        if (Userid,) in data:
            cursor.execute('select email from admin where Userid=%s',[Userid])
            data=cursor.fetchone()[0]
            cursor.close()
            subject='reset password for {data}'
            body=f'Reset the password using{request.host+url_for("createpassword",token=token(Userid,180))}'
            sendmail(data,subject,body)
            flash('Reset link send to your mail')
            return redirect(url_for('Adminlogin'))
        else:
            return 'Invalid Userid'
    return render_template('forgotpassword.html')
@app.route('/createpassword/<token>',methods=['GET','POST'])
def createpassword(token):
    try:
        s=Serializer(app.config['SECRET_KEY'])
        Userid=s.loads(token)['user']
        if request.method=='POST':
            npass=request.form['npassword']
            cpass=request.form['cpassword']
            if npass==cpass:
                cursor=mysql.connection.cursor()
                cursor.execute('update admin set password=%s where Userid=%s',[npass,Userid])
                mysql.connection.commit()
                return 'password reset successfully'
            else:
                return 'password mismatch'
        return render_template('newpassword.html')
    except Exception as e:
        print(e)
        return 'Link expired try again'
@app.route('/Students',methods=['GET','POST'])
def Students():
    if session.get('User'):
        Studentname=session.get('User')
        cursor=mysql.connection.cursor()
        cursor.execute('select * from student')
        Students_data=cursor.fetchall()
        print(Students_data)
        cursor.close()
        return render_template('AddStudenttable.html',data=Students_data)
    else:
        return redirect(url_for('Adminlogin'))
@app.route('/AddStudents',methods=['GET','POST'])
def AddStudents():
    if session.get('User'):
        if request.method=='POST':
            Studentid=request.form['Studentid']
            Studentname=request.form['Studentname']
            Course=request.form['Course']
            Roomno=request.form['Roomno']
            Mobileno=request.form['Mobileno']
            Email=request.form['Email']
            Address=request.form['Address']
            cursor=mysql.connection.cursor()
            cursor.execute('insert into student(Studentid,Studentname,Course,Roomno,Mobileno,Email,Address)values(%s,%s,%s,%s,%s,%s,%s)',[Studentid,Studentname,Course,Roomno,Mobileno,Email,Address])
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('Students'))
        return render_template('Students.html')
    else:
        return redirect(url_for('Adminlogin'))
@app.route('/update/<Studentid>',methods=['GET','POST'])
def update(Studentid):
    if session.get('User'):
        cursor=mysql.connection.cursor()
        cursor.execute('select * from student where Studentid=%s',[Studentid])
        Students_data=cursor.fetchone()
        print(Students_data)
        cursor.close()
        if request.method=='POST':
            Studentid=request.form['Studentid']
            Studentname=request.form['Studentname']
            Course=request.form['Course']
            Roomno=request.form['Roomno']
            Mobileno=request.form['Mobileno']
            Email=request.form['Email']
            Address=request.form['Address']
            cursor=mysql.connection.cursor()
            cursor.execute('update student set Studentid=%s,Studentname=%s,Course=%s,Roomno=%s,Mobileno=%s,Email=%s,Address=%s where Studentid=%s',[Studentid,Studentname,Course,Roomno,Mobileno,Email,Address,Studentid])
            mysql.connection.commit()
            cursor.close()
            flash('NOTES UPDATED SUCCESSFULLY')
            return redirect(url_for('Students'))
        return render_template('update.html',data=Students_data)
    else:
        return redirect(url_for('Adminlogin'))
@app.route('/delete/<Studentid>')
def delete(Studentid):
    cursor=mysql.connection.cursor()
    cursor.execute('delete from student where Studentid=%s',[Studentid])
    mysql.connection.commit()
    cursor.close()
    flash('Notes deletes successfully')
    return redirect(url_for('Students'))
@app.route('/checkin',methods=['GET','POST'])
def checkin():
    details=None
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * from student')
    data=cursor.fetchall()
    data1=request.args.get('Studentname') if request.args.get('Studentname') else 'empty'
    print(data1)
    cursor.execute('SELECT * from student where Studentid=%s',[data1])
    details=cursor.fetchone()
    cursor.execute('SELECT date,id,name,Roomno,Course,Mobileno,checkin,checkout from records')
    records=cursor.fetchall()
    cursor.close()
    if request.method=='POST':
        print(request.form)
        id=request.form['id']
        name=request.form['name']
        Course=request.form['Course']
        Roomno=request.form['Roomno']
        Mobileno=request.form['Mobileno']
        cursor=mysql.connection.cursor()
        today=date.today()
        day=today.day
        month=today.month
        year=today.year
        today_date=datetime.strptime(f'{year}-{month}-{day}','%Y-%m-%d')
        date_today=datetime.strftime(today_date,'%Y-%m-%d')
        cursor.execute('select count(*) from records where id=%s',[id])
        count=int(cursor.fetchone()[0])
        if id=="":
            flash('Select The student Studentid first')
        elif count>=1:
            flash('The student already gone outside')
        else:
            cursor=mysql.connection.cursor()
            cursor.execute('insert into records(date,id,name,Course,Roomno,Mobileno) values(%s,%s,%s,%s,%s,%s)',[date_today,id,name,Course,Roomno,Mobileno])
            mysql.connection.commit()
            cursor.execute('select date,id,name,Course,Roomno,Mobileno,checkin,checkout from records')
            records=cursor.fetchall()
            cursor.close()
    return render_template('Check(in-out).html',data1=data1,data=data,details=details,records=records)
@app.route('/checkoutupdate/<date>/<id1>')
def checkoutupdate(date,id1):
    cursor=mysql.connection.cursor()
    cursor.execute('update records set checkout=current_timestamp() where id=%s and date=%s',[id1,date])
    mysql.connection.commit()
    return redirect(url_for('checkin'))
@app.route('/checkinupdate/<date>/<id1>')
def checkinupdate(date,id1):
    cursor=mysql.connection.cursor()
    cursor.execute('update records set checkin=current_timestamp() where date=%s and id=%s',[date,id1])
    mysql.connection.commit()
    return redirect(url_for('checkin'))
@app.route('/checkoutvisitor/<id1>')
def checkoutvisitor(id1):
    cursor=mysql.connection.cursor()
    cursor.execute('update visitor set checkout=current_timestamp() where Studentid=%s',[id1])
    mysql.connection.commit()
    return redirect(url_for('visitor'))
@app.route('/checkinvisitor/<id1>')
def checkinvisitor(id1):
    cursor=mysql.connection.cursor()
    cursor.execute('update visitor set checkin=current_timestamp() where Studentid=%s',[id1])
    mysql.connection.commit()
    return redirect(url_for('visitor'))
@app.route('/visitor',methods=['GET','POST'])
def visitor():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * from student')
    data=cursor.fetchall()
    cursor.execute('Select * from visitor')
    details=cursor.fetchall()
    cursor.close()
    if request.method=="POST":
        Studentid=request.form['Studentid']
        name=request.form['name']
        mobilenumber=request.form['mobilenumber']
        cursor=mysql.connection.cursor()
        cursor.execute('INSERT INTO visitor(Studentid,name,mobilenumber) values(%s,%s,%s)',[Studentid,name,mobilenumber])
        cursor.execute('Select * from visitor')
        details=cursor.fetchall()
        mysql.connection.commit()
    return render_template('VisitorRecord.html',data=data,details=details)
app.run(use_reloader=True,debug=True)
