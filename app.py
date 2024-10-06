from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError  
from model import predict_lung_cancer  

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Database URI
app.config['SECRET_KEY'] = 'your_secret_key'  # Secret key for session management

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User model for the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# Prediction model for storing predictions
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Float, nullable=False)
    gender = db.Column(db.Float, nullable=False)
    smoking = db.Column(db.Float, nullable=False)
    yellow_fingers = db.Column(db.Float, nullable=False)
    anxiety = db.Column(db.Float, nullable=False)
    peer_pressure = db.Column(db.Float, nullable=False)
    chronic_disease = db.Column(db.Float, nullable=False)
    fatigue = db.Column(db.Float, nullable=False)
    allergy = db.Column(db.Float, nullable=False)
    wheezing = db.Column(db.Float, nullable=False)
    alcohol_consuming = db.Column(db.Float, nullable=False)
    coughing = db.Column(db.Float, nullable=False)
    shortness_of_breath = db.Column(db.Float, nullable=False)
    swallowing_difficulty = db.Column(db.Float, nullable=False)
    chest_pain = db.Column(db.Float, nullable=False)
    prediction_result = db.Column(db.String(50), nullable=False)

    def __init__(self, username, age, gender, smoking, yellow_fingers, anxiety, peer_pressure, chronic_disease,
                 fatigue, allergy, wheezing, alcohol_consuming, coughing, shortness_of_breath, swallowing_difficulty,
                 chest_pain, prediction_result):
        self.username = username
        self.age = age
        self.gender = gender
        self.smoking = smoking
        self.yellow_fingers = yellow_fingers
        self.anxiety = anxiety
        self.peer_pressure = peer_pressure
        self.chronic_disease = chronic_disease
        self.fatigue = fatigue
        self.allergy = allergy
        self.wheezing = wheezing
        self.alcohol_consuming = alcohol_consuming
        self.coughing = coughing
        self.shortness_of_breath = shortness_of_breath
        self.swallowing_difficulty = swallowing_difficulty
        self.chest_pain = chest_pain
        self.prediction_result = prediction_result

# Decorator to check if user is logged in
def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:  # Check if user is logged in
            flash('You need to login first!', 'danger')
            return redirect(url_for('login'))  # Redirect to login page
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@app.route('/')
def home():
    return render_template('home.html')  # Render home page

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Basic validation
        if not username or not password:
            flash('Username and password are required!', 'danger')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  # Hash password

        # Try to create a new user
        try:
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)  # Add user to the database
            db.session.commit()  # Commit changes
            flash('Registration successful, please log in.', 'success')  # Flash success message
            return redirect(url_for('login'))  # Redirect to login page
        except IntegrityError:
            db.session.rollback()  # Rollback the session if there's an error
            flash('Username already exists. Please choose a different username or <a href="/login">log in here</a>.', 'danger')  # Flash error message with link

    return render_template('register.html')  # Render registration page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Basic validation
        if not username or not password:
            flash('Username and password are required!', 'danger')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()  # Query for user

        if user and bcrypt.check_password_hash(user.password, password):  # Verify password
            session['username'] = user.username  # Set session variable
            flash('Login successful!', 'success')  # Flash success message
            return redirect(url_for('input_data'))  # Redirect to input data page
        else:
            flash('Login failed, check your username or password', 'danger')  # Flash error message
    
    return render_template('login.html')  # Render login page

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove user from session
    flash('You have been logged out.', 'info')  # Flash info message
    return redirect(url_for('login'))  # Redirect to login page

@app.route('/input', methods=['GET', 'POST'])
@login_required  # Ensure user is logged in
def input_data():
    if request.method == 'POST':
        # Receive input features from the form
        gender = 1 if request.form['GENDER'] == 'M' else 0  # Convert M/F to 1/0
        age = float(request.form['AGE'])
        smoking = float(request.form['SMOKING'])
        yellow_fingers = float(request.form['YELLOW_FINGERS'])
        anxiety = float(request.form['ANXIETY'])
        peer_pressure = float(request.form['PEER_PRESSURE'])
        chronic_disease = float(request.form['CHRONIC DISEASE'])
        fatigue = float(request.form['FATIGUE'])
        allergy = float(request.form['ALLERGY'])
        wheezing = float(request.form['WHEEZING'])
        alcohol_consuming = float(request.form['ALCOHOL CONSUMING'])
        coughing = float(request.form['COUGHING'])
        shortness_of_breath = float(request.form['SHORTNESS OF BREATH'])
        swallowing_difficulty = float(request.form['SWALLOWING DIFFICULTY'])
        chest_pain = float(request.form['CHEST PAIN'])

        # Create a list of features for prediction
        features = [
            gender,
            age,
            smoking,
            yellow_fingers,
            anxiety,
            peer_pressure,
            chronic_disease,
            fatigue,
            allergy,
            wheezing,
            alcohol_consuming,
            coughing,
            shortness_of_breath,
            swallowing_difficulty,
            chest_pain
        ]

        predicted_result = predict_lung_cancer(features)  # Call the prediction function

        # Convert prediction result to a readable string
        result_text = "Has Lung Cancer" if predicted_result == 1 else "No Lung Cancer"

        # Save the prediction to the database
        new_prediction = Prediction(
            username=session['username'],
            age=age,
            gender=gender,
            smoking=smoking,
            yellow_fingers=yellow_fingers,
            anxiety=anxiety,
            peer_pressure=peer_pressure,
            chronic_disease=chronic_disease,
            fatigue=fatigue,
            allergy=allergy,
            wheezing=wheezing,
            alcohol_consuming=alcohol_consuming,
            coughing=coughing,
            shortness_of_breath=shortness_of_breath,
            swallowing_difficulty=swallowing_difficulty,
            chest_pain=chest_pain,
            prediction_result=result_text
        )
        
        db.session.add(new_prediction)  # Add prediction to the database
        db.session.commit()  # Commit changes

        return render_template('result.html', result=predicted_result)  # Render result page

    return render_template('input.html')  # Render input page for GET request

@app.route('/history')
@login_required
def history():
    user_predictions = Prediction.query.filter_by(username=session['username']).all()  # Retrieve predictions for the user
    return render_template('history.html', predictions=user_predictions)  # Render history page

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all database tables
    app.run(debug=True)  # Run the Flask app
