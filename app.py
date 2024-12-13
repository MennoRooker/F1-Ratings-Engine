"""
Flask application for F1
"""

import os

from flask import Flask, render_template
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

    driver_ratings = (
        db.session.query(
            Rating.race_id,
            Race.name.label("race_name"),
            Rating.driver_id,
            Driver.name.label("driver_name"),
            Rating.adjusted_points.label("points"),
        )
        .join(Driver, Rating.driver_id == Driver.id)
        .join(Race, Rating.race_id == Race.id)
        .filter(Race.year == year)
        .order_by(Rating.driver_id, Rating.race_id)  # Order by driver and race
        .all()
    )

    # Build a dictionary to group points by driver
    driver_data = {}
    for row in driver_ratings:
        driver_name = row.driver_name
        race_name = row.race_name
        points = row.points

        if driver_name not in driver_data:
            driver_data[driver_name] = {
                "driver": driver_name,
                "races": [],
                "points": [],
                "cumulative_points": 0,
            }
        
        driver_data[driver_name]["races"].append(race_name)  # Add race name to x-axis
        driver_data[driver_name]["cumulative_points"] += points
        driver_data[driver_name]["points"].append(driver_data[driver_name]["cumulative_points"])    

    # Convert driver_data to a list of dicts for Plotly
    plot_data = list(driver_data.values())

    print(plot_data)

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

    return render_template("leaderboard.html", year=year, standings=aggregate_ratings, plot_data=plot_data)


if __name__ == "__main__":
    with app.app_context():  
        with app.test_request_context():
            print(leaderboard(2020))  