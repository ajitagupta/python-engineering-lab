from flask import Flask, request, jsonify
import db

app = Flask(__name__)

db.init_db()

@app.get('/workouts')
def get_workouts():
    sport = request.args.get("sport")
    min_distance = request.args.get("min_distance")
    if min_distance is not None:
        min_distance = float(min_distance)
    min_duration = request.args.get("min_duration")
    if min_duration is not None:
        min_duration = float(min_duration)

    return jsonify(db.search_workouts(sport, min_distance, min_duration))

@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid request body or empty body. Must be JSON."}), 400
    if data.get("sport") is None or data.get("sport") == "":
        return jsonify({"error": "The key sport is missing or empty. Must be swim, run, badminton, cycle, strength, or rest."}), 400

    allowed_sports = ["swim", "run", "badminton", "cycle", "strength", "rest"]
    sport = data["sport"]
    if sport not in allowed_sports:
        return jsonify({"error": "The key sport is invalid. Must be swim, run, badminton, cycle, strength, or rest."}), 400

    optional_distance = data.get("distance_km")
    optional_duration = data.get("duration_min")
    if optional_duration is None and (sport in ["run", "swim", "cycle", "badminton", "strength"]):
        return jsonify({"error": "The key duration_min is missing."}), 400
    if optional_distance is None and (sport in ["run", "swim", "cycle"]):
        return jsonify({"error": "The key distance_km is missing."}), 400

    if optional_duration is not None and not isinstance(optional_duration, (int, float)):
        return jsonify({"error": "The key duration_min must be a number."}), 400
    if optional_distance is not None and not isinstance(optional_distance, (int, float)):
        return jsonify({"error": "The key distance_km must be a number."}), 400

    if optional_duration is not None and optional_duration < 0:
        return jsonify({"error": "The key duration_min must be a positive number or 0."}), 400
    if optional_distance is not None and optional_distance < 0:
        return jsonify({"error": "The key distance_km must be a positive number or 0."}), 400


    return jsonify(db.add_workout(data))

@app.get('/workouts/<int:workout_id>')
def get_workout_by_id(workout_id):

    workout = db.get_workout_by_id(workout_id)
    if workout is None:
        return jsonify({"error": "Workout not found."}), 404

    return jsonify(workout)


if __name__ == "__main__":
    app.run(debug=True)