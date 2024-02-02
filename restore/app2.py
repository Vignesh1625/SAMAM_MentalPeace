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





#adding question to database code
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