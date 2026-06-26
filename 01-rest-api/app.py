from flask import Flask, request, jsonify

app = Flask(__name__)

workouts = ["run", "swim", "badminton", "strength", "run", "rest", "swim"]

@app.get('/workouts')
def get_workouts():
    return jsonify(workouts)

@app.route("/workouts", methods=["POST"])
def create_workout():
    return jsonify(request.get_json())


if __name__ == "__main__":
    app.run(debug=True)