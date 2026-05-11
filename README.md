# Personal Fitness Tracker

This is a simple web app built for casual and hardcore workout enthusiasts to track their exercises and progress.
The intent is remove the need to handcarry a physical notebook/jpurnal.


## Team Members

D'Eriq Sanders- Full Stack Developer  
Daniel Dzioba- Backend Developer (Python)  
Emmanuel James- N/A  
Bryston Buggs- N/A  

## Technologies Used

- Python 3.8+
- Flask 3.0.0
- Requests 2.31.0
- Firebase Auth REST API
- Firestore Database
- Tailwind CSS
  for guidance on how to use, visit: https://tailwindcss.com/docs/styling-with-utility-classes

## Project Objectives Assessment

### Provide a simple, no-frills utility to track fitness  
**Status:** Met  

**Explanation:** This intent was met as the UI is straightfoward and has all the bare essentials of a fitness tracker.  
User has a calender on the homepage that highlights the dates they worked out.  

### Give a free, accessible alternative to using a physical journal  
**Status:** Met  

**Explanation:** The application is free. This solution is able to be used on a computer/ mobile device to log workouts as opposed to a notebook. 

### Increase the number of individuals acheiving their fitness goals  
**Status:** Partially Met

**Explanation:** At this stage of the project this isnt quantifiable.  
Once application is fully deployed, metrics can be recorded to detemrine if fitness goals being achieved increased


## Features Implemented

Check off the features you implemented (must have at least 4 and 2 are implemeted for you already):

- [X] Feature #1: Login and Register
- [X] Feature #2: Log a workout
- [X] Feature #3: Set new goal
- [] Feature #4: Save and load preset



## Installation and Setup

### Prerequisites
- Python 3.8 or higher installed
- pip (Python package manager)

### Steps to Run

1. Clone or download this repository

2. Navigate to the project directory in your terminal:
   ```
   cd projectName
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your web browser and go to:
   ```
   http://localhost:5000
   ```

## Usage Instructions

User can type in email and password and click "Login" button to go to the home page.  
User can click the "New User?" button to create an account.  
User can click "Start New Workout..." to add an exercise.  
User can click "Create a Goal" to create a goal  

## Known Issues and Future Enhancements

Since the authentication isn't actually verifying a token, to test out the page access control, user will have to go to the login page and insert incorrect credentials for the application to detect that the user isn't logged in. This would be the most immediate improvement made to the app, to restrict application acess based off the user session token provided by Firebase.  

The database needs to modified so that data displayed in the application is user-unique.

The add workout feature needs a function that will allow the user to change the weight for each set.  



## API Endpoints Used

- `POST https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=[API_KEY]` - Sign up
- `POST https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=[API_KEY]` - Sign in



## Author

D'Eriq Sanders & Daniel Dzioba
