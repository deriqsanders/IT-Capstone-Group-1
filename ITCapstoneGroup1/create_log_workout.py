from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# ==========================
# Initialize App
# ==========================

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# ==========================
# Create
# ==========================

@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.json

    if not data.get("name") or not data.get("date") or not data.get("userId"):
        return jsonify({"error": "Missing required fields"}), 400

    workout_data = {
        "name": data["name"],
        "date": data["date"],  # format: YYYY-MM-DD
        "userId": data["userId"],
        "createdAt": datetime.utcnow()
    }

    doc_ref = db.collection("workouts").add(workout_data)

    return jsonify({
        "message": "Workout created",
        "workoutId": doc_ref[1].id
    }), 201


# ==========================
# Add Excercise
# ==========================

@app.route("/workouts/<workout_id>/exercises", methods=["POST"])
def add_exercise(workout_id):
    data = request.json

    required_fields = ["name", "weight", "sets", "reps"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing exercise fields"}), 400

    exercise_data = {
        "name": data["name"],
        "weight": float(data["weight"]),
        "sets": int(data["sets"]),
        "reps": int(data["reps"]),
        "createdAt": datetime.utcnow()
    }

    db.collection("workouts") \
      .document(workout_id) \
      .collection("exercises") \
      .add(exercise_data)

    return jsonify({"message": "Exercise added"}), 201


# ==========================
# Fetch Workout
# ==========================

@app.route("/workouts/<workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout_doc = db.collection("workouts").document(workout_id).get()

    if not workout_doc.exists:
        return jsonify({"error": "Workout not found"}), 404

    workout_data = workout_doc.to_dict()

    exercises = db.collection("workouts") \
                  .document(workout_id) \
                  .collection("exercises") \
                  .stream()

    exercise_list = []
    for e in exercises:
        ex = e.to_dict()
        ex["id"] = e.id
        exercise_list.append(ex)

    return jsonify({
        "id": workout_id,
        **workout_data,
        "exercises": exercise_list
    })


# ==========================
# Update Workout
# ==========================

@app.route("/workouts/<workout_id>", methods=["PUT"])
def update_workout(workout_id):
    data = request.json

    db.collection("workouts").document(workout_id).update(data)

    return jsonify({"message": "Workout updated"})


# ==========================
# Delete Workout
# ==========================

@app.route("/workouts/<workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    db.collection("workouts").document(workout_id).delete()
    return jsonify({"message": "Workout deleted"})


# ==========================
# List User Workouts
# ==========================

@app.route("/users/<user_id>/workouts", methods=["GET"])
def get_user_workouts(user_id):
    workouts = db.collection("workouts") \
                 .where("userId", "==", user_id) \
                 .stream()

    workout_list = []
    for w in workouts:
        workout_data = w.to_dict()
        workout_data["id"] = w.id
        workout_list.append(workout_data)

    return jsonify(workout_list)


if __name__ == "__main__":
    app.run(debug=True)
