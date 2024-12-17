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


# ============================================ CONSTRUCTORS ============================================ #
def get_constructor_standings(race_id, season):
    """Retrieve constructor standings up to a specific race in a season."""

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


# ============================================= PENALTIES ============================================= #
def assign_penalties(standings):
    """Assign penalties based on the constructor standings."""

    penalties = {}  # Define an empty dictionary for assigning penalties

    for rank, standing in enumerate(standings, start=1):
        penalty = 10 - rank + 1
        penalties[standing.constructor_id] = penalty

    return penalties


# ============================================== RATINGS ============================================== #
def populate_ratings(race, penalties, season, is_first_race):
    """Populate the ratings table for a specific race, applying penalties."""

    results = (
        db.session.query(Result)
        .filter(Result.race_id == race.id)
        .all()
    )

    for result in results:
        driver_id = result.driver_id
        constructor_id = result.constructor_id

        if is_first_race:
            adjusted_points = result.points

        # Calculate adjusted points
        penalty = penalties.get(constructor_id, 0)
        points = result.points
        adjusted_points = result.points - penalty

        # Set zero-sum rating to 0
        zero_sum_rating = 0

        # Create a new rating entry
        rating = Rating(
            driver_id=driver_id,
            constructor_id=constructor_id,
            race_id=race.id,
            year=season,
            points=points,
            adjusted_points=adjusted_points,
            zero_sum_rating=zero_sum_rating
        )
        db.session.add(rating)

    db.session.commit()


# ============================================== SEASONS ============================================== #
def process_season(season):
    """Process the season and populate the ratings table with adjusted points --
    All pre-2010 seasons will adopt the post-2010 scoring system and the post-2010 seasons
    will not include fastest laps or sprint races for consistency reasons"""

    # Introduce post-2010 scoring system to apply to all seasons
    scoring_system = {
        1: 25,
        2: 18,
        3: 15,
        4: 12,
        5: 10,
        6: 8,
        7: 6,
        8: 4,
        9: 2,
        10: 1
    }

    # Get all results for all races
    results = db.session.query(Result).all()
    
    # Change results to match post-2010 scoring system
    for result in results:
        if result.position is None:
            result.points = 0
        else:
            result.points = scoring_system.get(result.position, 0)  # Default to 0 for positions > 10

    # Commit changes to the database
    db.session.commit()
    print("Points updated to post-2010 scoring system.")
   
    races = (
        db.session.query(Race)
        .filter_by(year=season)
        .order_by(Race.id)
        .all()
    )

    print(f"\nGenerating adjusted points for {season} season\n")

    # Iterate over the races in a season and apply penalties where needed
    for i, race in enumerate(races):
        
        print(f"\nProcessing Race {race.id} - {race.name}")
        standings = get_constructor_standings(race.id - 1, season)
        penalties = assign_penalties(standings)

        if i == 0:
            populate_ratings(race, penalties, season, is_first_race=True)  # No penalties for the first race
        else:
            populate_ratings(race, penalties, season, is_first_race=False)  

    print(f"\n{season} season processing complete!")


# =============================================== MAIN =============================================== #
if __name__ == "__main__":
    with app.app_context():
        for year in range(1950,2024):
            process_season(season=year)
