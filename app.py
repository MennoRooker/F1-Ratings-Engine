"""
Main ratings engine for determining drivers' ratings
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

# ======================================== LEADERBOARD ======================================== #
@app.route("/")
def leaderboard():
    driver_points_2020 = (
        db.session.query(Driver.name, func.sum(Result.points).label("total_points"))
        .join(Result, Driver.id == Result.driver_id)
        .join(Race, Result.race_id == Race.id)
        .filter(Race.year == 2020)
        .group_by(Driver.id)
        .order_by(func.sum(Result.points).desc())  # Order by total points, descending
        .all()
    )

    return render_template("leaderboard.html", standings=driver_points_2020)