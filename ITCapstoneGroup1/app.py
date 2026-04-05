
from collections import Counter

import firebase_admin
from flask import Flask, redirect, request, render_template, url_for, current_app, g
import json
import requests
import datetime
from datetime import date, timedelta

import firebase_admin
from firebase_admin import credentials, firestore, auth 

import os
from dotenv import load_dotenv




load_dotenv('itcapstone.env')

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
        uid = response_data.get('localId')
        print(f"UID: {uid}")
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

    currentdate = datetime.datetime.now().strftime("%m-%d")

    todaysdate = date.today()
    breakstreakdate = todaysdate - timedelta(days=2)

    workout_ref = db.collection('workouts')
    docs = workout_ref.stream()

    goal_ref = db.collection('goals')
    goal_docs = goal_ref.stream()

    gdate = u'goaldate'
    global goal_dates
    goal_dates = []
    

    for doc in goal_docs:
           
        doc_dict = doc.to_dict()
       
        if gdate in doc_dict:
            print(f"Goal date: {doc_dict[gdate]}")
            goal_dates.append(doc_dict[gdate])  
            
        else:
            print("No date field found in document.")

    dates = u'date'
    highlighted_dates = []
    
    for doc in docs:
           
        doc_dict = doc.to_dict()
       
        if dates in doc_dict:
            print(f"Workout date: {doc_dict[dates]}")
            highlighted_dates.append(doc_dict[dates])  
            
        else:
            print("No date field found in document.")

    counts = Counter(highlighted_dates).keys()
    workouttotal = len(counts)
    print(workouttotal)
    
    datesinorder = sorted(highlighted_dates)
    lastdate = datesinorder[-1]
    print(currentdate)
    totaldistance = workout_ref.where('distance', '!=', '').stream()
    totaldistance = sum(float(doc.to_dict().get('distance', 0)) for doc in totaldistance)
    print(totaldistance)
    
    lastWorkoutDate = datetime.datetime.strptime(lastdate, "%m-%d").date()
    lastWorkoutDatewithyear = lastWorkoutDate.replace(year=todaysdate.year)
    print(lastWorkoutDatewithyear)
    if lastWorkoutDatewithyear > breakstreakdate:
        streak = "🔥"
    else:
        streak = "❄️"
    
    print(streak)
    
    
    return render_template('home.html', workouttotal=workouttotal, highlighted_dates=highlighted_dates, streak=streak, totaldistance=totaldistance, goal_dates=goal_dates)

@app.route('/home', methods=['POST'])
def add_goal():
    goals_ref = db.collection('goals')
    goalname = request.form.get('goalname')
    goalmonth = request.form.get('goalmonth')
    goalday = request.form.get('goalday')
    goaldate = f"{int(goalmonth):02d}-{int(goalday):02d}"

   
    

    global goal_dates
    

  

    if goaldate in goal_dates:
        print("Goal already exists.")
        return redirect(url_for('home'))
    else:

     goals_ref.add({
        "goalname": goalname,
        "goaldate": goaldate
    })
    return redirect(url_for('home'))
   

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
    distance = request.form.get('distance')
    time = request.form.get('time')

    workout_ref = db.collection('workouts')

    workout_ref.add( {
        "date": date,
        "name": name,
        "weight": weight,
        "sets": sets,
        "repetitions": repetitions,
        "distance": distance,
        "time": time
    })
    return redirect(url_for('exercise'))

      

           
if __name__ == "__main__":
    app.run(debug=True)
