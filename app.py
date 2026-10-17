from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load travel destination data
with open("data/destinations.json", "r") as file:
    destinations = json.load(file)


def generate_itinerary(destination, days, budget, interest):

    destination_data = destinations.get(destination)

    if not destination_data:
        return None

    itinerary = []

    places = destination_data["places"]
    activities = destination_data["activities"]
    food = destination_data["food"]

    for day in range(1, days + 1):

        # Select a place based on user's interest
        selected_place = None

        for place in places:
            if interest.lower() in place["type"].lower():
                selected_place = place
                break

        # If no matching place is found
        if selected_place is None:
            selected_place = places[(day - 1) % len(places)]

        day_plan = {
            "day": day,
            "morning": selected_place["name"],
            "afternoon": activities[(day - 1) % len(activities)],
            "evening": food[(day - 1) % len(food)],
            "budget": budget
        }

        itinerary.append(day_plan)

    return itinerary


@app.route("/", methods=["GET", "POST"])
def home():

    itinerary = None

    if request.method == "POST":

        destination = request.form["destination"]
        days = int(request.form["days"])
        budget = request.form["budget"]
        interest = request.form["interest"]

        itinerary = generate_itinerary(
            destination,
            days,
            budget,
            interest
        )

    return render_template(
        "index.html",
        destinations=destinations.keys(),
        itinerary=itinerary
    )


if __name__ == "__main__":
    app.run(debug=True)