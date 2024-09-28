ActivePython 2.7.18.4 (ActiveState Software Inc.) based on
Python 2.7.18.4 (default, Aug  9 2021, 23:37:24) [MSC v.1500 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return "Login Page"

@app.route('/register')
def register():
    return "Register Page"

@app.route('/input')
def input_data():
    return "Input Data Page"

if __name__ == '__main__':
    app.run(debug=True)
