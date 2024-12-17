"""
Flask application for F1
"""

import os

from flask import Flask, render_template, jsonify, request
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
    """Displays the points and adjusted ratings of all drivers that participated in a season
    and plots their scores over time"""

    # Check if the penalties tick-box is applied from the query parameter
    apply_penalties = request.args.get("apply_penalties", "false").lower() == "false"

    # Get all races for the given year
    all_races = (
        db.session.query(Race.id, Race.name)
        .filter(Race.year == year)
        .order_by(Race.id)
        .all()
    )

    # Convert race list to a dictionary for easier lookup
    race_lookup = [{race.id: race.name} for race in all_races]

    # Build a dictionary to group points by driver
    driver_data = {}

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

    def with_or_without_penalties(apply_penalties):
        """Returns the regular points if user has not ticked 'With Penalties' box, and 
        returns adjusted points if the box IS ticked"""

        # Populate points for each race
        for race in all_races:
            for driver in all_drivers:
                
                if apply_penalties:
                    # Query for the adjusted points
                    rating = (
                        db.session.query(Rating.adjusted_points)
                        .filter(
                            Rating.race_id == race.id,
                            Rating.driver_id == driver.id,
                        )
                        .scalar()
                    )

                else:
                    # Query for the regular points
                    rating = (
                        db.session.query(Rating.points)
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

        return driver_data.values()

    # Convert driver_data to a list of dicts for Plotly
    plot_data = list(with_or_without_penalties(apply_penalties))

    aggregate_ratings = (
        db.session.query(
            Driver.name,
            func.sum(Rating.points).label("points"),
            func.sum(Rating.adjusted_points).label("adjusted_points"),
            func.sum(Rating.zero_sum_rating).label("zero_sum_rating")
        )
        .join(Rating, Driver.id == Rating.driver_id)
        .join(Race, Rating.race_id == Race.id)
        .filter(Race.year == year)
        .group_by(Driver.id)
        .order_by(func.sum(Rating.adjusted_points).desc())  # Order by adjusted points
        .all()
    )

    return render_template(
        "leaderboard.html",
        year=year,
        standings=aggregate_ratings,
        plot_data=plot_data,
        race_lookup=race_lookup,
        apply_penalties=apply_penalties
    )



# ============================================ DRIVER NAMES ============================================ #
@app.route('/api/drivers', methods=['GET'])
def get_drivers():
    """Creates an API route to store all 800+ Formula 1 drivers"""
    
    # Query all driver names for the comparisons
    drivers = db.session.query(Driver.name).distinct().all()
    driver_names = [driver[0] for driver in drivers]
    
    return jsonify(driver_names)


# ========================================== AVAILABLE YEARS ========================================== #
@app.route('/api/years', methods=['GET'])
def get_years_for_driver():
    """Creates an API route to store the active years for specific drivers"""

    driver_name = request.args.get('driver_name')
    if not driver_name:
        return jsonify([])
    
    # Query all years the driver participated
    years = (
        db.session.query(Race.year)
        .join(Rating, Rating.race_id == Race.id)
        .join(Driver, Driver.id == Rating.driver_id)
        .filter(Driver.name == driver_name)
        .distinct()
        .order_by(Race.year)
        .all()
    )
    year_list = [year[0] for year in years]

    return jsonify(year_list)


# ============================================ COMPARISONS ============================================ #
@app.route("/season-compare", methods=["GET", "POST"])
def season_compare():

    if request.method == "POST":

        # Get the drivers and years from the form
        driver1_name = request.form.get("driver1_name")
        year1 = int(request.form.get("year1"))
        driver2_name = request.form.get("driver2_name")
        year2 = int(request.form.get("year2"))

        # Function to fetch driver data for a specific year and driver
        def fetch_driver_data(driver_name, year):
            # Fetch all races for the specified year
            races = (
                db.session.query(Race.id, Race.name)
                .filter(Race.year == year)
                .order_by(Race.id)
                .all()
            )

            # Initialize the driver data structure
            driver_data = {
                "driver": f"{driver_name} ({year})",
                "races": [],  # x-axis: race names
                "points": [],  # y-axis: cumulative points
                "cumulative_points": 0,
            }

            # Populate points for each race
            cumulative_points = 0
            for race in races:
                # Fetch the points for this driver in the current race
                rating = (
                    db.session.query(func.sum(Rating.adjusted_points))
                    .join(Driver, Rating.driver_id == Driver.id)
                    .filter(
                        Driver.name == driver_name,
                        Rating.race_id == race.id,
                    )
                    .scalar()
                )

                # If no points exist, assume the driver didn't participate
                if rating is None:
                    rating = 0

                # Update cumulative points and race data
                cumulative_points += rating
                driver_data["races"].append(race.name)  # Add race name to x-axis
                driver_data["points"].append(cumulative_points)  # Append cumulative points

            return driver_data

        # Fetch data for both drivers
        driver1_data = fetch_driver_data(driver1_name, year1)
        driver2_data = fetch_driver_data(driver2_name, year2)

        # Prepare plot data
        plot_data = [driver1_data, driver2_data]


        # Render the comparison template with the plot data
        return render_template("compare.html", plot_data=plot_data)

    # Render the input form for GET requests
    return render_template("compare.html")



# ============================================ FETCH NAMES ============================================ #
def fetch_names(year):
    """Test function"""

    driver_names = (
        db.session.query(Driver.name)
        .join(Rating, Driver.id == Rating.driver_id)
        .join(Race, Rating.race_id == Race.id)
        .filter(Race.year == year)
        .distinct()  # Ensure unique driver names
        .all()
    )

    return [name[0] for name in driver_names]


# ================================================ MAIN ================================================ #
if __name__ == "__main__":
    with app.app_context():  
        with app.test_request_context():
            leaderboard(2020)
            print(fetch_names(2020))