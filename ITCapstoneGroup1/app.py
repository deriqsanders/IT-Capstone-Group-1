
from flask import Flask, redirect, request, render_template, url_for
import json
import requests


app = Flask(__name__)

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
            'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyC5qMt0Vy5E86A9ZhHYUeiNj6YtJpQGh4I',
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
            'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyC5qMt0Vy5E86A9ZhHYUeiNj6YtJpQGh4I',
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
    return render_template('home.html') 
      
           
if __name__ == "__main__":
    app.run(debug=True)