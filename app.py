from flask import Flask, render_template, request,session,jsonify
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from datetime import datetime
import geocoder
import requests
import json
import pickle
import pytz
import bcrypt
import joblib


app = Flask(__name__)
app.secret_key = "778031a659c117f6ab82986676e24271"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SamamDataBase.db'
db = SQLAlchemy(app)

def get_current_date():
    return datetime.now(pytz.timezone('Asia/Kolkata')).date()

def get_current_time():
    return datetime.now(pytz.timezone('Asia/Kolkata')).time()

#creating a table in our database
class UserDetails(db.Model):
    email = db.Column(db.String(120),primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    date = db.Column(db.Date, nullable=False, default=get_current_date)
    time = db.Column(db.Time, nullable=False, default=get_current_time)
    latitude = db.Column(db.Float, unique=False, nullable=False,default=100)
    longitude = db.Column(db.Float, unique=False, nullable=True,default=100)

    def __repr__(self):
        return f'<User {self.name}>'

class CharacterQuestions(db.Model):
    id = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    question = db.Column(db.String(1000), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.id}>'
class DisorderQuestions(db.Model):
    id = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    question = db.Column(db.String(1000), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.id}>'
    
#creating a table to store the result of the users
class CharacterResult(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(80), unique=False, nullable=False)
    result = db.Column(db.String(80), unique=False, nullable=False)
    date = db.Column(db.Date, nullable=False, default=get_current_date)
    time = db.Column(db.Time, nullable=False, default=get_current_time)

    def __repr__(self):
        return f'<User {self.email}>'
class DisorderResult(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(80), unique=False, nullable=False)
    result = db.Column(db.String(80), unique=False, nullable=False)
    date = db.Column(db.Date, nullable=False, default=get_current_date)
    time = db.Column(db.Time, nullable=False, default=get_current_time)

    def __repr__(self):
        return f'<User {self.email}>'
    


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(60), nullable=False)
    salt = db.Column(db.String(29), nullable=False)

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password, salt

def store_user(email, password):
    hashed_password, salt = hash_password(password)
    new_user = User(email=email, hashed_password=hashed_password, salt=salt)
    db.session.add(new_user)
    db.session.commit()

def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), user.salt)
        return hashed_password == user.hashed_password
    return False


api_key = "0c6367c0ffc59182e0e17fbbe7ced418"
latitude = 0.0
longitude = 0.0
#loding models

atmospherePickle = joblib.load('./Models/atmosphereModel.joblib')
characterPickle = joblib.load('./Models/characterModel.joblib')
disorderPickle = joblib.load('./Models/disorderModel.joblib')

def celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

def get_weather(api_key, lat, lon):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}lat={lat}&lon={lon}&appid={api_key}"

    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        if "main" in data:
            main_data = data["main"]
            temperature = main_data.get("temp", "N/A") - 273.15  # Convert Kelvin to Celsius
            humidity = main_data.get("humidity", "N/A")

            #print(f"Temperature: {temperature:.2f}°C")
            #print(f"Humidity: {humidity}%")
            return temperature, humidity
        else:
            return "Unexpected response structure. Data structure may have changed. Response:"
    else:
        return "Weather data not available for this location!"

@app.route('/')
def home():
    users = UserDetails.query.all()
    return render_template('./loginPage.html')

@app.route('/Page2')
def page2():
    return render_template('Page2.html')

@app.route('/register')
def register():
    return render_template('./mainPage.html')

@app.route('/register_form', methods=['GET', 'POST'])
def registerPage():
    name = request.form.get('name')
    email = request.form.get('email')
    age_str = request.form.get('age')
    gender = request.form.get('gender')
    password = request.form.get('password')
    try:
        age = int(age_str)
    except ValueError:
        return "Invalid age value. Please enter a valid number."

    
    try:
        #check if user already exists
        if db.session.query(UserDetails.query.filter_by(email=email).exists()).scalar() :
            return render_template('./mainPage.html',error="Email already exists")
        store_user(email, password)
        new_user = UserDetails(
            email=email,
            name=name,
            age=age,
            gender=gender,
            password=password,
        )

        db.session.add(new_user)
        db.session.commit()
        session['user_email'] = new_user.email 
        UserDetails.query.all()
        #print("User added to database")
        return redirect(url_for('page2'))
    except Exception as e:
        #print("Error in adding user to database")
        return render_template('./mainPage.html',error="Error in adding user to database"+str(e))  


@app.route('/login_form', methods=['GET', 'POST'])
def login_form():
    email = request.form.get('email')
    password = request.form.get('password')
    if verify_password(email, password):
        user = UserDetails.query.filter_by(email=email).first()
        session['user_email'] = user.email
        return redirect(url_for('page2'))
    else:
        return render_template('./loginPage.html',error="Incorrect email or password")
    
@app.route('/account', methods=['GET', 'POST'])
def account():
    try:
        user_email = session.get('user_email')
        user = UserDetails.query.get(user_email)
        if user_email == 'eligetivignesh@gmail.com':
            return redirect(url_for('adminPage'))
        charResult = CharacterResult.query.filter_by(email=user_email).all()
        disResult = DisorderResult.query.filter_by(email=user_email).all()
        return render_template('./account.html',user = user,
                               charResult = charResult,
                               disResult = disResult
                               )
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return render_template('./loginPage.html')


@app.route('/adminPage', methods=['GET', 'POST'])
def adminPage():
    user_email = session.get('user_email')
    user = UserDetails.query.get(user_email)
    CharQuestions = CharacterQuestions.query.all()
    users = UserDetails.query.all()
    DisQuestions = DisorderQuestions.query.all()
    return render_template('./adminPage.html',user=user, users=users,CharacterQuestions=CharQuestions,DisorderQuestions=DisQuestions)



@app.route('/edit_question/<int:question_id>', methods=['PUT'])
def edit_question(question_id):
    try :
        data = request.json
        newQuestionText = request.json['questionText']
        tableId = request.json['tableId']

        #print(newQuestionText,tableId)
        if tableId == 'CharacterQuestionsTable':
            ques = CharacterQuestions.query.get(question_id)
        elif tableId == 'DisorderQuestionsTable':
            ques = DisorderQuestions.query.get(question_id)
        else :
            print("Error in table id")
        ques.question = newQuestionText
        db.session.commit()
        return jsonify({"message": "Question edited successfully"}), 200
    except Exception as e:
        return jsonify(error=str(e)), 500
    
    
# delete user from database
@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = UserDetails.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)  # pass the user object
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200



@app.route('/character_form', methods=['GET', 'POST'])
def character_form():
    questions  = CharacterQuestions.query.all()
    #for i in range (0,len(questions)):
    #    print(questions[i].question)

    return render_template('./CharacterQuestions.html',questions = questions)

@app.route('/disorder_form', methods=['GET', 'POST'])
def disorder_form():
    questions  = DisorderQuestions.query.all()
    #for i in range (0,len(questions)):
    #    print(questions[i].question)

    return render_template('./DisorderQuestions.html',questions = questions)

@app.route('/character_submit', methods=['GET', 'POST'])	
def characterSubmit():
    user_email = session.get('user_email')
    user = UserDetails.query.get(user_email)
    questions = CharacterQuestions.query.all()
    noOfQuestions = len(questions)
    question_array = [0] * noOfQuestions
    try:
        for i in range (0,noOfQuestions):
            question_array[i] = int(request.form.get("question "+str(questions[i].id)))

        if len(question_array) != 5:
            return "Error in number of questions with feature array"
        if user.gender == 'male' :
            features = [2, user.age] + question_array
        else :
            features = [1, user.age] + question_array
        result = characterPickle.predict([features])
        label_mapping = {
                          0 : 'dependable',
                          1 : 'extraverted',
                          2 :'lively',
                          3 :'responsible',
                          4 : 'serious'
                        }
        
        #storing the result in the database
        new_result = CharacterResult(
            email=user_email,
            result=label_mapping[result[0]],
        )
        db.session.add(new_result)
        db.session.commit()

        result = "Your character prediction is "+label_mapping[result[0]]
        return render_template('./resultPage.html', result=result, Name=user.name, gender=user.gender)
    except ValueError:
        return "Please enter valid numbers for the questions."

@app.route('/disorder_submit', methods=['GET', 'POST'])
def disorderSubmit():
    user_email = session.get('user_email')  
    latest_user = UserDetails.query.get(user_email)
    questions = DisorderQuestions.query.all()
    noOfQuestions = len(questions)
    question_array = [0] * noOfQuestions
    try:
        for i in range(0,noOfQuestions):
            question_array[i] = int(request.form.get("question"+str(questions[i].id)))
        if len(question_array) != 26:
            return "Error in number of questions with feature array"
        features = question_array + [latest_user.age]
        result = disorderPickle.predict([features])
        label_mapping = { 0 : '89+gfADHD',
                          1 : 'ASD',
                          2 : 'Loneliness',
                          3 : 'MDD',
                          4 : 'OCD',
                          5 : 'PDD',
                          6 : 'PTSD',
                          7 : 'anexiety',
                          8 : 'bipolar',
                          9 : 'eating disorder',
                         10 : 'psychotic deprission',
                         11 :'sleeping disorder'
                        }
        result_int = int(result)
        disorder_name = label_mapping[result_int]

        #storing the result in the database
        new_result = DisorderResult(
            email=user_email,
            result=disorder_name,
        )
        db.session.add(new_result)
        db.session.commit()

        result = f"You have {disorder_name} disorder"
        return render_template('./resultPage.html',result=result,Name = latest_user.name, gender = latest_user.gender)
    except ValueError:
        return "Please enter valid numbers for the questions."



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)