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
    """Retrieve constructor standings up to a specific race."""
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
    """Assign penalties based on the constructor standings."""
    penalties = {}
    for rank, standing in enumerate(standings, start=1):
        penalty = 10 - rank + 1
        penalties[standing.constructor_id] = penalty
    return penalties

def populate_ratings_for_race(race, penalties, season):
    """Populate the ratings table for a specific race, applying penalties."""
    results = (
        db.session.query(Result)
        .filter(Result.race_id == race.id)
        .all()
    )

    for result in results:
        driver_id = result.driver_id
        constructor_id = result.constructor_id

        # Calculate adjusted points
        penalty = penalties.get(constructor_id, 0)
        adjusted_points = result.points - penalty

        # Calculate zero-sum rating
        zero_sum_rating = 0

        # Create a new rating entry
        rating = Rating(
            driver_id=driver_id,
            constructor_id=constructor_id,
            race_id=race.id,
            year=season,
            adjusted_points=adjusted_points,
            zero_sum_rating=zero_sum_rating
        )
        db.session.add(rating)

    db.session.commit()


def add_points_first_race(race, season):
    """Add the points for the first race without penalties."""
    # Query the results for the first race
    results = (
        db.session.query(Result)
        .filter(Result.race_id == race.id)
        .all()
    )

    for result in results:
        driver_id = result.driver_id
        constructor_id = result.constructor_id

        # Points are not adjusted for the first race (penalty = 0)
        adjusted_points = result.points
        zero_sum_rating = 0

        # Create a new rating entry for the first race
        rating = Rating(
            driver_id=driver_id,
            constructor_id=constructor_id,
            race_id=race.id,
            year=season,
            adjusted_points=adjusted_points,
            zero_sum_rating=zero_sum_rating
        )
        db.session.add(rating)

    db.session.commit()


def process_season(season):
    """Process the season and populate the ratings table with adjusted points."""
    races = (
        db.session.query(Race)
        .filter_by(year=season)
        .order_by(Race.id)
        .all()
    )

    print(f"\nGenerating adjusted points for {season} season\n")

    for i, race in enumerate(races):
        
        print(f"\nProcessing Race {race.id} - {race.name}")
        standings = get_constructor_standings(race.id - 1, season)
        penalties = assign_penalties(standings)

        if i == 0:
            add_points_first_race(race, season)  # Still add the points from the first race
            continue

        populate_ratings_for_race(race, penalties, season)

    print("\nSeason processing complete!")

# Run script to populate the ratings table
if __name__ == "__main__":
    with app.app_context():
        process_season(season=2020)
