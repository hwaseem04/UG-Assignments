from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3


app = Flask(__name__)
app.secret_key = "text123"

# Function to validate username and password
def validate(username, password):
    """
    --> New user is created if user doesn't exist.
    --> If existing user enters wrong password, then the user won't be redirected to any page.
    """
    
    conn = sqlite3.connect('../database.db')
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM user;')

    data = cur.fetchall()
    flag = 0
    for USER, PASS in data:
        if USER == username:
            flag = 1
            if PASS == password:
                return 1
            else:
                break
    
    if flag != 1:
        cur.execute(f'INSERT INTO user VALUES("{username}", "{password}");')
        conn.commit()

    conn.close()
    return 0

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['user']
        password = request.form['pass']

        if username == '' or password == '':
            return redirect(url_for('index'))
        
        if validate(username, password):
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return redirect(url_for('index'))
        
    else:
        return render_template('index.html')

@app.route("/home", methods=["POST", "GET"])
def home():
    if 'user' in session:
        return render_template('home.html', user=session['user'])
    else:
        return render_template('index.html')

@app.route("/mnist")
def mnist():
    return render_template('mnist.html')

@app.route("/regression")
def regression():
    return render_template('regression.html')

@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user", None)
    return redirect(url_for('index'))
