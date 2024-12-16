"""
Flask application for F1
"""

import os

from flask import Flask, render_template, request
from flask_session import Session

from engine import *

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# ============================================= HOME PAGE ============================================= #
@app.route("/")
def homepage():

    # Creates a list of available seasons
    seasons = (
        db.session.query(Race.year)
        .distinct()
        .order_by(Race.year.desc())
        .all()
    )
    seasons = [year[0] for year in seasons]

    return render_template("homepage.html", seasons=seasons)


# ============================================ LEADERBOARD ============================================ #
@app.route("/<int:year>")
def leaderboard(year):

    # Build a dictionary to group points by driver
    driver_data = {}

    # Get all races for the given year
    all_races = (
        db.session.query(Race.id, Race.name)
        .filter(Race.year == year)
        .order_by(Race.id)
        .all()
    )

    # Convert race list to a dictionary for easier lookup
    race_lookup = [{race.id: race.name} for race in all_races]

    # print(race_lookup)

    # Get all drivers who participated in at least one race that year
    all_drivers = (
        db.session.query(Driver.id, Driver.name)
        .join(Rating, Driver.id == Rating.driver_id)
        .join(Race, Rating.race_id == Race.id)
        .filter(Race.year == year)
        .distinct()
        .all()
    )

    # Initialize driver data structure
    for driver in all_drivers:
        driver_data[driver.name] = {
            "driver": driver.name,
            "races": [],
            "points": [],
            "cumulative_points": 0,
        }

    # Populate points for each race
    for race in all_races:
        for driver in all_drivers:
            # Check if this driver has points for this race
            rating = (
                db.session.query(Rating.adjusted_points)
                .filter(
                    Rating.race_id == race.id,
                    Rating.driver_id == driver.id,
                )
                .scalar()
            )

            # If no rating exists, assume the driver didn't participate
            if rating is None:
                rating = 0

            # Update the driver's data
            driver_name = driver.name
            driver_data[driver_name]["races"].append(race.name)  # Add race name to x-axis
            driver_data[driver_name]["cumulative_points"] += rating  # Add cumulative points
            driver_data[driver_name]["points"].append(driver_data[driver_name]["cumulative_points"]) 

    # Convert driver_data to a list of dicts for Plotly
    plot_data = list(driver_data.values())

    # print(plot_data)

    aggregate_ratings = (
        db.session.query(
            Driver.name,
            func.sum(Rating.adjusted_points).label("total_points"),
            func.sum(Rating.zero_sum_rating).label("zero_sum_rating")
        )
        .join(Rating, Driver.id == Rating.driver_id)
        .join(Race, Rating.race_id == Race.id)
        .filter(Race.year == year)
        .group_by(Driver.id)
        .order_by(func.sum(Rating.adjusted_points).desc())  # Order by adjusted points
        .all()
    )

    return render_template("leaderboard.html", year=year, standings=aggregate_ratings, plot_data=plot_data, race_lookup=race_lookup)


# ============================================ COMPARISONS ============================================ #
@app.route("/season-compare", methods=["GET", "POST"])
def season_compare():
    if request.method == "POST":
        # Get the drivers and years from the form
        driver1_name = request.form.get("driver1_name")
        year1 = int(request.form.get("year1"))
        driver2_name = request.form.get("driver2_name")
        year2 = int(request.form.get("year2"))

        # Fetch data for driver 1
        driver1_data = (
            db.session.query(
                Race.id.label("race_id"),
                Race.year.label("year"),
                func.sum(Rating.adjusted_points).label("points")
            )
            .join(Rating, Race.id == Rating.race_id)
            .join(Driver, Rating.driver_id == Driver.id)
            .filter(Driver.name == driver1_name, Race.year == year1)
            .group_by(Race.id)
            .order_by(Race.id)
            .all()
        )

        # Fetch data for driver 2
        driver2_data = (
            db.session.query(
                Race.id.label("race_id"),
                Race.year.label("year"),
                func.sum(Rating.adjusted_points).label("points")
            )
            .join(Rating, Race.id == Rating.race_id)
            .join(Driver, Rating.driver_id == Driver.id)
            .filter(Driver.name == driver2_name, Race.year == year2)
            .group_by(Race.id)
            .order_by(Race.id)
            .all()
        )

        # Convert data to plot format
        def prepare_plot_data(driver_data):
            races = list(range(1, len(driver_data) + 1))  # Number races sequentially
            points = [row.points for row in driver_data]
            return {"races": races, "points": points}

        plot_data = {
            "driver1": {
                "name": f"{driver1_name} ({year1})",
                **prepare_plot_data(driver1_data),
            },
            "driver2": {
                "name": f"{driver2_name} ({year2})",
                **prepare_plot_data(driver2_data),
            },
        }

        return render_template("compare.html", plot_data=plot_data)

    # Render the input form for GET requests
    return render_template("compare.html")



if __name__ == "__main__":
    with app.app_context():  
        with app.test_request_context():
            leaderboard(2020)