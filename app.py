"""
Flask application for F1
"""

import os

from flask import Flask, render_template, session, request
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
    # Query for the driver standings based on the ratings table
    driver_ratings = (
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

    # Render the leaderboard page with the query results
    return render_template("leaderboard.html", standings=driver_ratings, year=year)



