from flask import Flask, render_template, request,session
from flask_sqlalchemy import SQLAlchemy
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
    longitude = db.Column(db.Float, unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    

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
        new_user = UserDetails(
            username=name,
            email=email,
            age=age,
            gender=gender,
            latitude=lat,
            longitude=lon
        )
        db.session.add(new_user)
        db.session.commit()
        UserDetails.query.all()
        print("User added to database")
    except :
        print("Error in adding user to database")
    

    if 10 <= age < 20:
        return render_template('./teenPage.html')
    elif 20 <= age < 40:
        return render_template('./adultPage.html')
    else:
        return render_template('./oldPage.html')
    

@app.route('/teenAgeSubmit', methods=['GET', 'POST'])
def teenAgeSubmit():
    print("lat :", latitude, "long :", longitude)
    tempature,humidity = get_weather(api_key, latitude, longitude)
    q1 = int(request.form.get('question1'))
    q2 = int(request.form.get('question2'))
    q3 = int(request.form.get('question3'))
    q4 = int(request.form.get('question4'))
    q5 = int(request.form.get('question5'))
    q6 = request.form.get('question6')

    tempature = celsius_to_fahrenheit(tempature)
    atmospherePrediction = atmospherePickle.predict([[humidity,tempature,q6]])
    print("atmospherePrediction Stress Level:",atmospherePrediction)

    result = q1+q2+q3+q4+q5
    return render_template('./resultPage.html', result=result, atmospherePrediction=atmospherePrediction, Name=session.get('name'),gender = session.get('gender'))

@app.route('/adultAgeSubmit', methods=['GET', 'POST'])
def adultAgeSubmit():
    print("lat :", latitude, "long :",  longitude)
    tempature,humidity = get_weather(api_key, latitude,  longitude)
    q1 = int(request.form.get('question1'))
    q2 = int(request.form.get('question2'))
    q3 = int(request.form.get('question3'))
    q4 = int(request.form.get('question4'))
    q5 = int(request.form.get('question5'))
    q6 = request.form.get('question6')
    
    tempature = celsius_to_fahrenheit(tempature)
    atmospherePrediction = atmospherePickle.predict([[humidity,tempature,q6]])
    print("atmospherePrediction Stress Level:",atmospherePrediction)

    result = q1+q2+q3+q4+q5
    return render_template('./resultPage.html', result=result, atmospherePrediction=atmospherePrediction, Name=session.get('name'),gender = session.get('gender'))

@app.route('/oldAgeSubmit', methods=['GET', 'POST'])
def oldAgeSubmit():
    print("lat :", latitude, "long :",  longitude)
    tempature,humidity = tempature,humidity = get_weather(api_key, latitude,  longitude)
    q1 = int(request.form.get('question1'))
    q2 = int(request.form.get('question2'))
    q3 = int(request.form.get('question3'))
    q4 = int(request.form.get('question4'))
    q5 = int(request.form.get('question5'))
    q6 = request.form.get('question6')

    tempature = celsius_to_fahrenheit(tempature)
    atmospherePrediction = atmospherePickle.predict([[humidity,tempature,q6]])
    print("atmospherePrediction Stress Level:",atmospherePrediction)

    result = q1+q2+q3+q4+q5
    return render_template('./resultPage.html', result=result, atmospherePrediction=atmospherePrediction, Name=session.get('name'),gender = session.get('gender'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)