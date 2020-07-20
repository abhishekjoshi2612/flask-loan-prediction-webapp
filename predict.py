import os
import numpy as np
from flask import Flask, render_template, url_for, redirect,request,flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_table import Table
from flask_migrate import Migrate
import jinja2
import pickle

app = Flask(__name__)
models = pickle.load(open('model.pkl','rb'))
app.config['SECRET_KEY'] = 'mysecret'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods = ['GET','POST'])
def predict():
    if request.method == "POST":
        myform = request.form
        #print(request.form["ApplicantIncome"])
        for key in myform:
            if key is None:
                return render_template('home.html')
        mde = []
        for ele in myform:
            mde.append(request.form[ele])
        mde.append(0)
        for index, ele in enumerate(mde):
            if ele == "Male":
                mde[index] = 1
            if ele == "Female":
                mde[index] = 0
            if ele == "YES":
                mde[index] = 1
            if ele =="NO":
                mde[index] = 0
        mde = [mde]
        mde = np.asarray(mde,dtype='float64')
        ans = models.predict(mde)

    return render_template('output.html',ans = ans)



if __name__ == "__main__":
    app.run(debug=True)
