"""
Main ratings engine for determining drivers' ratings
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
    print(f"Standings after Race {race_id}:")
    for standing in standings:
        print(f"Constructor: {standing.constructor_name}, Points: {standing.total_points}")
    return standings

def assign_penalties(standings):
    penalties = {}
    print("\nPenalties Based on Standings:")
    for rank, standing in enumerate(standings, start=1):
        penalty = max(10 - rank + 1, 0)  # Top 10 constructors only
        penalties[standing.constructor_id] = penalty
        print(f"{standing.constructor_name}: -{penalty} points")
    return penalties

def adjust_driver_points_for_race(race_id, penalties):
    results = (
        db.session.query(Result)
        .join(Driver, Result.driver_id == Driver.id)
        .filter(Result.race_id == race_id)
        .all()
    )

    print(f"\nAdjusting points for Race {race_id}:")
    for result in results:

        # Checking where I get an object of 'NoneType'
        print(f"Result ID: {result.id}")
        print(f"Driver: {result.driver}")
        if result.driver:
            print(f"Driver Name: {result.driver.name}")
            print(f"Constructor: {result.constructor.name}")
            if result.constructor:
                print(f"Constructor Name: {result.constructor.name}")

        # Continuing with the actual logic
        constructor_id = result.constructor_id
        penalty = penalties.get(constructor_id, 0)
        adjusted_points = result.points - penalty
        print(
            f"Driver: {result.driver.name}, Constructor: {result.constructor.name}, "
            f"Original Points: {result.points}, Penalty: -{penalty}, Adjusted Points: {adjusted_points}"
        )
        result.points = adjusted_points
        db.session.add(result)

    db.session.commit()

def process_season(season):
    races = (
        db.session.query(Race)
        .filter_by(year=season)
        .order_by(Race.id)
        .all()
    )

    for i, race in enumerate(races):
        if i == 0:
            print(f"Skipping Race {race.id} (No constructor standings yet)")
            continue

        print(f"\nProcessing Race {race.id} - {race.name}")
        standings = get_constructor_standings(race.id - 1, season)
        penalties = assign_penalties(standings)
        adjust_driver_points_for_race(race.id, penalties)

    print("\nSeason processing complete!")

# Run script to add the data
if __name__ == "__main__":
    with app.app_context():
        process_season(season=2020)