# Personal Fitness Tracker

This is a simple web app built for casual and hardcore workout enthusiasts to track their exercises and progress.

## Features Implemented

Check off the features you implemented (must have at least 4 and 2 are implemeted for you already):

- [X] Feature #1: Login and Register
- [] Feature #2: Log a workout
- [] Feature #3: Set new goal
- [] Feature #4: Save and load preset

## Technologies Used

- Python 3.8+
- Flask 3.0.0
- Requests 2.31.0
- Firebase Auth REST API
- Tailwind CSS

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

## Usage

User can type in email and password and click "Login" button to go to the home page.
User can click the "New User?" button to create an account.

## Screenshots


## API Endpoints Used

- `POST https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=[API_KEY]` - Sign up
- `POST https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=[API_KEY]` - Sign in



## Author

D'Eriq Sanders
