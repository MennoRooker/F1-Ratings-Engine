"""
Main ratings engine for 'F1-ELO-Engine-2.0' repository
"""

import os

from flask import Flask
from sqlalchemy.sql import func


from models import *

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def get_constructor_standings(race_id, season=2020):
    # Sum points for each constructor up to the given race
    standings = (
        db.session.query(
            Constructor.id.label("constructor_id"),
            Constructor.name.label("constructor_name"),
            func.sum(Result.points).label("total_points")
        )
        .join(Result, Constructor.id == Result.constructor_id)
        .join(Race, Result.race_id == Race.id)
        .filter(Race.year == season, Race.id <= race_id)
        .group_by(Constructor.id, Constructor.name)
        .order_by(func.sum(Result.points).desc())
        .all()
    )
    return standings

def assign_penalties(standings):
    penalties = {}
    for rank, standing in enumerate(standings, start=1):
        penalties[standing.constructor_id] = max(10 - rank+1, 0)
    return penalties

def adjust_driver_points_for_race(race_id, penalties):
    results = (
        db.session.query(Result)
        .join(Driver, Result.driver_id == Driver.id)
        .filter(Result.race_id == race_id)
        .all()
    )

    for result in results:
        constructor_id = result.driver.constructor_id
        penalty = penalties.get(constructor_id, 0)
        result.points -= penalty
        db.session.add(result)

    db.session.commit()

def process_season(season=2020):
    # Get all races in the season
    races = (
        db.session.query(Race)
        .filter_by(year=season)
        .order_by(Race.id)
        .all()
    )

    for i, race in enumerate(races):
        if i == 0:
            continue  # Skip the first race

        # Get standings after the previous race
        standings = get_constructor_standings(race.id - 1, season)
        penalties = assign_penalties(standings)

        # Adjust points for the current race
        adjust_driver_points_for_race(race.id, penalties)

# Run script to add the data
if __name__ == "__main__":
    with app.app_context():
        get_constructor_standings(1031)