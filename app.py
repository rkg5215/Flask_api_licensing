from flask import Flask, render_template, request, redirect, session,get_flashed_messages, flash
import mysql.connector
import os


app=Flask(__name__)
app.secret_key=os.urandom(24)

conn= mysql.connector.connect(host="localhost", user="root", password="Batman", database="flasklogin")
cursor= conn.cursor()


@app.route('/')
def home():
    return render_template("main.html")


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/dashboard')
def dashboard():
    if session.get('user_id'):
        return render_template("dashboard.html")
    
    else:
        return redirect('/login')
    

@app.route('/login_validation', methods =['POST'])
def login_validation():
    username=request.form.get('uname')
    password=request.form.get('psw')
    
    cursor.execute("""Select * from users where username LIKE '{}' AND password LIKE '{}'""".format(username, password))
    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']= users[0][0]
        return redirect ('/dashboard')
    else:
        flash("Invalid credentials. Check your account username and password")
        return redirect ('/login')
        

@app.route('/add_user', methods =['POST'])
def add_user():
    name=request.form.get('rname')
    email=request.form.get('remail')
    username=request.form.get('runame')
    password=request.form.get('rpsw')
    
    cursor.execute("""Select * from users where username LIKE '{}' OR email LIKE '{}'""".format(username, email))
    users=cursor.fetchall()
    if len(users)>0:
        flash("That username or email is already used, please choose another")
        return redirect('/register')
    else:
        cursor.execute("""INSERT INTO users (name, email, username, password) 
                            VALUES 
                            ('{}','{}','{}','{}') """.format(name, email, username, password))
        conn.commit()
        flash("User Registered Successfully")
        return redirect ('/dashboard')
       

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/login')


if __name__== '__main__':
    app.run(debug=True)