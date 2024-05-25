from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moh.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Moh(db.Model):
    sno = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.DateTime, default = datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        user = Moh.query.filter_by(username = username).first()
        if user:
            return render_template('signup.html', account = True)
        elif password != confirm_password:
            return render_template('signup.html', matched = True)
        elif not user and password == confirm_password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = Moh(username=username,email=email,password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
    return render_template('signup.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_username = request.form['username']
        password = request.form['password']    
        user = Moh.query.filter_by(username= user_username).first()
        if not user or not bcrypt.check_password_hash(user.password, password):
            return render_template("login.html", login = True)
        if user and bcrypt.check_password_hash(user.password, password):
            return render_template('index.html', logedin='True')

    return render_template('login.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')


if __name__ == "__main__":
    app.run(debug=True)

