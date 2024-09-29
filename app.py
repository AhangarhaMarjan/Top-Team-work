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
