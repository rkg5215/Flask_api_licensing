from flask import Flask, render_template, request, redirect, session, flash, jsonify
import mysql.connector
import os
import random


app=Flask(__name__)
app.secret_key=os.urandom(24)

conn= mysql.connector.connect(host="localhost", user="root", password="Batman", database="flasklogin")
cursor= conn.cursor()


@app.route('/')
def home():
    return render_template("main.html")


@app.route('/login')
def login():
    if session.get('user_id'):   # Check session exists or not
        return redirect("/dashboard") 
    else:
        return render_template("login.html")
    

@app.route('/register')
def register():
    if session.get('user_id'):
        return redirect("/dashboard") 
    else:
        return render_template("register.html")


# ----------User Login(User Login Validation)----------------

@app.route('/login_validation', methods =['POST'])
def login_validation():
    username=request.form.get('uname')
    password=request.form.get('psw')
    
    cursor.execute("""Select * from users where username LIKE '{}' AND password LIKE '{}'""".format(username, password))
    users=cursor.fetchall()  #--Fetch All data from database
    if len(users)>0:         # if matches then a tuple gets in output if not then blank tuple
        session['user_id']= users[0][1]  # Create a session with existing username or make with userid
        flash("Login Successfull")
        return redirect ('/dashboard')
    else:
        flash("Invalid credentials. Check your account username and password")
        return redirect ('/login')
        
# ----------User Register(Adding a new user)----------------

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
        return redirect ('/login')


# ----------License Key Generation------

def key_generate():
    key=''
    section= ''
    alphabet= 'ABCDEFHGIJKLMNOPQRSTUVWXYZ1234567890'

    # key format  = aaaa-bbbb-cccc-1111 or 24 Char
    while len(key)<25:
        char = random.choice(alphabet) # Randomly pick from digit
    # add random to choice key
        key += char
    # Also add in random choice to section upto 4
        section +=char
    # Add a DASHES/Hypen
        if len(section)==4:
            key +='-' # add in hyphen
            section = ''  # Reset the section to nothing
    key= key[:-1]   # set key to all but the last digit

    # output the key
    license_key = key
    user_name=session.get('user_id') 
    return render_template("dashboard.html", license_key=license_key,user=user_name) 
    # return redirect("/dashboard") 

@app.route('/dashboard')
def dashboard():
    if session.get('user_id'):    
        return key_generate()        
    else:
        return redirect('/login')


@app.route('/users')
def get_users():
    mysql_query = """SELECT * from users"""
    cursor.execute(mysql_query)
    datas=cursor.fetchall()
    final=[]
    for data in datas:
        result = {
                "User_id": data[0],
                "Name": data[1],
                "Email": data[2],
                "Username" : data[3]
            }
        final.append(result)

    return jsonify({"All_Users" : final})

@app.route('/users/<string:username>')
def get_specific(username):
    mysql_query = """SELECT * from users"""
    cursor.execute(mysql_query)
    datas=cursor.fetchall()
    for data in datas:
        if username==data[3]:
            result = {
                "User_id": data[0],
                "Name": data[1],
                "Email": data[2],
                "Username" : data[3]
            }
            return jsonify(result)
        
    return "The User does not exist !! Please Register First"

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/login')


if __name__== '__main__':
    app.run(debug=True)


    # """SELECT * from users where username = hello """