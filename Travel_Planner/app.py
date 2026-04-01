from flask import Flask, render_template, request, jsonify
from travel_agents import generate_travel_plan

app = Flask(__name__)

@app.route("/")
def default():
    return render_template("index.html")

@app.route("/travel_planner",methods=["POST"])
def travel_planner():
    try:
        destination = request.form.get("destination")
        budget = request.form.get("budget")
        interests = request.form.get("interests")
        time_of_year = request.form.get("time_of_year")

        results = generate_travel_plan(destination, budget, interests, time_of_year)

        response = {
            "destination_recommendation": results[0],
            "itinerary": results[1],
            "budget_tips": results[2]
        }

        return jsonify(response)
    
    except Exception as e :
        return jsonify({"error" : str((e))}), 500

if __name__ == "__main__":
    app.run(debug=True)





