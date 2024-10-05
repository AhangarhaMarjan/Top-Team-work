# ActivePython 2.7.18.4 (ActiveState Software Inc.) based on
# Python 2.7.18.4 (default, Aug  9 2021, 23:37:24) [MSC v.1500 32 bit (Intel)] on win32
# Type "help", "copyright", "credits" or "license()" for more information.
import pickle
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
    
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
    return render_template('input.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        features = [float(request.form['mean_radius']),
                    float(request.form['mean_concavity']),
                    float(request.form['mean_concave_points']),
                    float(request.form['texture_error']),
                    float(request.form['worst_radius']),
                    float(request.form['worst_smoothness'])]
        
        input_data = np.array(features).reshape(1, -1)
        prediction = model.predict(input_data)
        result = 'Cancerous' if prediction[0] == 1 else 'Non-cancerous'
        return render_template('result.html', prediction=result)


if __name__ == '__main__':
    app.run(debug=True)
