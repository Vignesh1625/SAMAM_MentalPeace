from flask import Flask, render_template, request,session,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from datetime import datetime
import geocoder
import requests
import json
import pickle
import pytz


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
    id = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    date = db.Column(db.Date, nullable=False, default=get_current_date)
    time = db.Column(db.Time, nullable=False, default=get_current_time)
    latitude = db.Column(db.Float, unique=False, nullable=False)
    longitude = db.Column(db.Float, unique=False, nullable=True,default=100)

    def __repr__(self):
        return f'<User {self.username}>'

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

api_key = "0c6367c0ffc59182e0e17fbbe7ced418"
latitude = 0.0
longitude = 0.0
#loding models
with open('./data/atmospherepickle.pkl', 'rb') as f:
    atmospherePickle = pickle.load(f)

with open('./data/characterpicle.pkl', 'rb') as f:
    characterPickle = pickle.load(f)
    
with open('./data/disorderpickle.pkl', 'rb') as f:
    disorderPickle = pickle.load(f)

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

            print(f"Temperature: {temperature:.2f}°C")
            print(f"Humidity: {humidity}%")
            return temperature, humidity
        else:
            return "Unexpected response structure. Data structure may have changed. Response:"
    else:
        return "Weather data not available for this location!"

@app.route('/')
def home():
    users = UserDetails.query.all()
    return render_template('./mainPage.html')

@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    name = request.form.get('name')
    age_str = request.form.get('age')
    gender = request.form.get('gender')
    email = request.form.get('email')

    #getting user location using ip address
    g = geocoder.ip('me')
    lat, lon = g.latlng
    latitude = lat
    longitude = lon
    print(f"lat: {lat}, long: {lon}")

    try:
        age = int(age_str)
    except ValueError:
        return "Invalid age value. Please enter a valid number."
    
    #adding new user to database
    try:
        print(f"latitude: {lat}, longtude: {lon}")

        new_user = UserDetails(
            username=name,
            email=email,
            age=age,
            gender=gender,
            latitude=lat,
            longitude=lon,
        )

        db.session.add(new_user)
        db.session.commit()
        UserDetails.query.all()
        print("User added to database")
    except :
        print("Error in adding user to database")
    

    return render_template('./Page2.html')
    


@app.route('/login_form', methods=['GET', 'POST'])
def loginPage():
    error = 'No'
    return render_template('./loginPage.html',error=error)


@app.route('/submit_login_form', methods=['GET', 'POST'])
def submit_login_form():
    email = request.form.get('username')
    password = request.form.get('password')
    print(email, password)
    if ( email == "eligetivignesh@gmail.com" or email == "Vignesh1625" ) and password == "Vignesh1625":
        return adminPage()
    else:
        return render_template('./loginPage.html',error="Yes")


@app.route('/adminPage', methods=['GET', 'POST'])
def adminPage():
    CharQuestions = CharacterQuestions.query.all()
    users = UserDetails.query.all()
    DisQuestions = DisorderQuestions.query.all()


    return render_template('./adminPage.html', users=users,CharacterQuestions=CharQuestions,DisorderQuestions=DisQuestions)


#adding question to database
@app.route('/add_question', methods=['POST'])
def add_question():
    try:
        data = request.json
        new_question = CharacterQuestions(id=data['id'], question=data['question'])
        db.session.add(new_question)
        db.session.commit()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

#adding question to database
@app.route('/add_Disquestions', methods=['POST'])
def add_Disquestion():
    try:
        data = request.json
        new_question = DisorderQuestions(id=data['id'], question=data['question'])
        db.session.add(new_question)
        db.session.commit()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(error=str(e)), 500
    
# delete question from database
@app.route('/delete_question/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = CharacterQuestions.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    db.session.delete(question)  # pass the question object
    db.session.commit()

    return jsonify({"message": "Question deleted successfully"}), 200


# delete question from database
@app.route('/deleteDis_question/<int:question_id>', methods=['DELETE'])
def deleteDis_question(question_id):
    question = DisorderQuestions.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    db.session.delete(question)  # pass the question object
    db.session.commit()

    return jsonify({"message": "Question deleted successfully"}), 200


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
    for i in range (0,len(questions)):
        print(questions[i].question)

    return render_template('./CharacterQuestions.html',questions = questions)

@app.route('/disorder_form', methods=['GET', 'POST'])
def disorder_form():
    questions  = DisorderQuestions.query.all()
    for i in range (0,len(questions)):
        print(questions[i].question)

    return render_template('./DisorderQuestions.html',questions = questions)

@app.route('/character_submit', methods=['GET', 'POST'])	
def characterSubmit():
    latest_user = UserDetails.query.order_by(UserDetails.id.desc()).first()
    questions = CharacterQuestions.query.all()
    noOfQuestions = len(questions)
    question_array = [0] * noOfQuestions
    try:
        for i in range (0,noOfQuestions):
            question_array[i] = int(request.form.get("question "+str(questions[i].id)))

        if len(question_array) != 5:
            return "Error in number of questions with feature array"
        if latest_user.gender == 'male' :
            features = [2, latest_user.age] + question_array
        else :
            features = [1, latest_user.age] + question_array
        result = characterPickle.predict([features])
        label_mapping = { 0 : 'dependable',
                          1 : 'extraverted',
                          2 :'lively',
                          3 :'responsible',
                          4 : 'serious'
                        }
        result = "Your character prediction is "+label_mapping[result[0]]
        return render_template('./resultPage.html', result=result, Name=latest_user.username, gender=latest_user.gender)
    except ValueError:
        return "Please enter valid numbers for the questions."

@app.route('/disorder_submit', methods=['GET', 'POST'])
def disorderSubmit():
    latest_user = UserDetails.query.order_by(UserDetails.id.desc()).first()
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
        label_mapping = { 0 : 'ADHD',
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
        result = f"You have {disorder_name} disorder"
        return render_template('./resultPage.html',result=result,Name = latest_user.username, gender = latest_user.gender)
    except ValueError:
        return "Please enter valid numbers for the questions."


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)