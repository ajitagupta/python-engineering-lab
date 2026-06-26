from flask import Flask, request, jsonify

app = Flask(__name__)

workouts = [{"sport": "run", "distance_km": 6.0}, {"sport": "swim", "distance_km": 0.2}, {"sport": "badminton", "duration_min": 90}, {"sport": "strength", "duration_min": 35}, {"sport": "run", "distance_km": 8.0}, {"sport": "rest"}, {"sport": "swim", "distance_km": 0.400}]

@app.get('/workouts')
def get_workouts():
    return jsonify(workouts)

@app.route("/workouts", methods=["POST"])
def create_workout():
    return jsonify(request.get_json())


if __name__ == "__main__":
    app.run(debug=True)