@app.route('/teenAgeSubmit', methods=['GET', 'POST'])
def teenAgeSubmit():
    # Retrieve the latest user details from the database
    latest_user = UserDetails.query.order_by(UserDetails.id.desc()).first()
    latitude = latest_user.latitude
    longitude = latest_user.longitude

    print("lat :", latitude, "long :", longitude)
    temperature, humidity = get_weather(api_key, latitude, longitude)
    q1 = int(request.form.get('question1'))
    q2 = int(request.form.get('question2'))
    q3 = int(request.form.get('question3'))
    q4 = int(request.form.get('question4'))
    q5 = int(request.form.get('question5'))
    q6 = request.form.get('question6')

    temperature = celsius_to_fahrenheit(temperature)
    atmospherePrediction = atmospherePickle.predict([[humidity, temperature, q6]])
    print("atmospherePrediction Stress Level:", atmospherePrediction)

    result = q1 + q2 + q3 + q4 + q5
    return render_template('./resultPage.html', result=result, atmospherePrediction=atmospherePrediction, Name=latest_user.username, gender=latest_user.gender)

@app.route('/adultAgeSubmit', methods=['GET', 'POST'])
def adultAgeSubmit():
    latest_user = UserDetails.query.order_by(UserDetails.id.desc()).first()
    latitude = latest_user.latitude
    longitude = latest_user.longitude

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
    return render_template('./resultPage.html', result=result, atmospherePrediction=atmospherePrediction, Name=latest_user.username, gender=latest_user.gender)

@app.route('/oldAgeSubmit', methods=['GET', 'POST'])
def oldAgeSubmit():
    latest_user = UserDetails.query.order_by(UserDetails.id.desc()).first()
    latitude = latest_user.latitude
    longitude = latest_user.longitude
    
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
    return render_template('./resultPage.html', result=result, atmospherePrediction=atmospherePrediction, Name=latest_user.username, gender=latest_user.gender)
