from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import ai_model

app = Flask(__name__)
app.secret_key = "d53cb57debad104fff7a382024d6cd9759c48ae567298a3c"  

app.config["MONGO_URI"] = "mongodb://localhost:27017/automotive_db"
mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = mongo.db.users.find_one({'username': username})

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        mongo.db.users.insert_one({'username': username, 'password': hashed_password})
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

@app.route('/complaint', methods=['GET', 'POST'])
def complaint():
    if request.method == 'POST':
        complaint_data = {
            'complaint_id': request.form['complaint_id'],
            'complaint_text': request.form['complaint_text'],
            'product_id': request.form['product_id'],
            'complaint_date': request.form['complaint_date'],
            'resolved': request.form['resolved']
        }
        mongo.db.complaints.insert_one(complaint_data)
        return redirect(url_for('home'))
    return render_template('complaint.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_data = {
            'feedback_id': request.form['feedback_id'],
            'feedback_text': request.form['feedback_text'],
            'product_id': request.form['product_id'],
            'feedback_date': request.form['feedback_date'],
            'rating': request.form['rating']
        }
        mongo.db.feedbacks.insert_one(feedback_data)
        return redirect(url_for('home'))
    return render_template('feedback.html')

@app.route('/improvements')
def improvements():
    complaints = list(mongo.db.complaints.find())
    feedbacks = list(mongo.db.feedbacks.find())

    improvements_text = ai_model.generate_improvements(complaints, feedbacks)
    improvements_list = [{'improvement': improvement} for improvement in improvements_text if improvement.strip()]

    return render_template('improvements.html', improvements=improvements_list)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
