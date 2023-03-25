from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import pickle
import torch
from torchvision import transforms
from PIL import Image
import os

app = Flask(__name__)
app.secret_key = "text123"

# Simple regression to predict salary with years of experience
def predict_salary(exp):
    import numpy as np
    exp = np.array([[exp]])
    model = pickle.load(open('../simpleregression.pkl', 'rb'))
    prediction = model.predict(exp)
    return prediction[0][0]

# Predict the digit
def predict(img):
    # Load image and convert to tensor
    img = Image.open(img)
    transform = transforms.ToTensor()
    img = transform(img)

    # model class object loaded
    modelClass = pickle.load(open('../classificationModel.pkl', 'rb'))

    # model checkpoint loaded
    model_dict = torch.load('../classificationCheckpoint.pt')

    # Setting the pretrained weights
    modelClass.load_state_dict(model_dict)
    modelClass.eval()

    # Output prediction
    prediction = modelClass(img.unsqueeze(0))
    prediction = torch.argmax(torch.softmax(prediction, axis=1), axis=1).item()

    return prediction

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

@app.route("/mnist", methods=["POST", "GET"])
def mnist():
    if "user" in session:
        path = r'static/images/mnist_data'
        files = os.listdir(path)
        files_path = []
        for file in files:
            files_path.append(os.path.join(path, file))

        
        if request.method == "POST":
            img_path = request.form['image']
            img_path = img_path.replace("http://127.0.0.1:5000/","" )
            prediction = predict(img_path)
            prediction = f'Predicted digit: {prediction}'
            return render_template('mnist.html', files=files_path, prediction=prediction, select_path=img_path)
        else:
            return render_template('mnist.html', files=files_path, select_path="static/images/mnist_data/img_1.jpg")
    return redirect(url_for('index'))

@app.route("/regression", methods=["POST", "GET"])
def regression():
    if "user" in session:
        if request.method == "POST":
            exp = float(request.form['exp'])
            prediction = predict_salary(exp)
            prediction = f'Predicted salary for {exp} years of experience is: {prediction:.4f}'
            return render_template('regression.html', prediction=prediction)
        else:
            
            return render_template('regression.html')
    return redirect(url_for('index'))


@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user", None)
    return redirect(url_for('index'))
