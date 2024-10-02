from flask import Flask, render_template, request
import numpy as np


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

# Input page route
@app.route('/input', methods=['GET', 'POST'])
def input_page():
    if request.method == 'POST':
        # Get the form data
        mean_radius = float(request.form['mean_radius'])
        mean_concavity = float(request.form['mean_concavity'])
        mean_concave_points = float(request.form['mean_concave_points'])
        texture_error = float(request.form['texture_error'])
        worst_radius = float(request.form['worst_radius'])
        worst_smoothness = float(request.form['worst_smoothness'])

        # Create an array of features for prediction
        features = np.array([[mean_radius, mean_concavity, mean_concave_points, texture_error, worst_radius, worst_smoothness]])

        # Redirect to result page with features
        return redirect(url_for('result_page', features=features))

    return render_template('input.html')

# Result page route
@app.route('/result', methods=['GET'])
def result_page():
    # Get features from URL parameters
    features = request.args.getlist('features', type=float)

    # Convert features to the right shape
    features = np.array([features])

    # Predict using the loaded model
    prediction = model.predict(features)

    # Display the result (1 for cancer, 0 for no cancer)
    result = 'Positive for Cancer' if prediction[0] == 1 else 'Negative for Cancer'

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
