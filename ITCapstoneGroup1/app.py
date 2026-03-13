
import firebase_admin
from flask import Flask, redirect, request, render_template, url_for, current_app, g
import json
import requests
import datetime

import firebase_admin
from firebase_admin import credentials, firestore  

import os
from dotenv import load_dotenv




load_dotenv('ITCapstoneGroup1/itcapstone.env')

api_key = os.getenv('API_KEY')


app = Flask(__name__)

cred = credentials.Certificate('.secrets/it-senior-capstone-group-1-firebase-adminsdk-fbsvc-01cdb49165.json')
firebase_admin.initialize_app(cred) 
#firebase_admin.initialize_app()
db = firestore.client()
collection = db.collection('workouts')
doc_ref = db.collection('workouts').document()




@app.route('/')
def index():
        

    return render_template('index.html')

@app.route('/signup')
def signup():
    
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup_user():
    email = request.form.get('email')
    password = request.form.get('password')

  

    print(f"Received email: {email}, password: {'*' * len(password) if password else None}")
    

    try:
        response = requests.post(
            f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}',
            data=json.dumps({
                'email': email,
                'password': password,
                'returnSecureToken': True
            }),
            headers={'Content-Type': 'application/json'}
        )
        response_data = response.json()
        print(f"Firebase response: {response_data}")

        if 'idToken' in response_data:
            print("Signup successful!")
            return redirect(url_for('home'))
        else:
            print("Signup failed.")
            return redirect(url_for('signup'))
    except Exception as e:
        print(f"Error during signup: {e}")
        return redirect(url_for('signup'))


@app.route('/', methods=['POST'])
def user_credentials():
    email = request.form.get('email')
    password = request.form.get('password')

    print(f"Received email: {email}, password: {'*' * len(password) if password else None}")
    
    try:
        response = requests.post(
            f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}',
            data=json.dumps({
                'email': email,
                'password': password,
                'returnSecureToken': True
            }),
            headers={'Content-Type': 'application/json'}
        )
        response_data = response.json()
        print(f"Firebase response: {response_data}")

        if 'idToken' in response_data:
            print("Login successful!")
            return redirect(url_for('home'))
        else:
            print("Login failed.")
            return redirect(url_for('index'))
    except Exception as e:
        print(f"Error during login: {e}")
        return redirect(url_for('index'))

   
@app.route('/home')
def home():

    workout_ref = db.collection('workouts')

    count_query = workout_ref.count()
    count_result = count_query.get()
    workout_count = count_result[0][0].value

    docs = workout_ref.stream()
    

    dates = u'date'
    highlighted_dates = []

    for doc in docs:
           
        

        
    
        doc_dict = doc.to_dict()
        
        if dates in doc_dict:
            print(f"Workout date: {doc_dict[dates]}")
            highlighted_dates.append(doc_dict[dates])
            json_string = json.dumps(highlighted_dates)
            print(json_string)
        else:
            print("No date field found in document.")

    print(f"Total workouts in Firestore: {workout_count}")

    
    return render_template('home.html', workout_count=workout_count, date_data=json_string, highlighted_dates=highlighted_dates)

@app.route('/exercise')
def exercise():

    return render_template('exercise.html')

@app.route('/exercise', methods=['POST'])
def add_exercise():

    date = datetime.datetime.now().strftime("%m-%d")
    name = request.form.get('name')
    weight = request.form.get('weight')
    sets = request.form.get('sets')
    repetitions = request.form.get('repetitions')

    workout_ref = db.collection('workouts')

    workout_ref.add( {
        "date": date,
        "name": name,
        "weight": weight,
        "sets": sets,
        "repetitions": repetitions
    })
    return redirect(url_for('exercise'))

      

           
if __name__ == "__main__":
    app.run(debug=True)