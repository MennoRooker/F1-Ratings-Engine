"""
Imports data from .csv files into the corresponding tables
"""

import csv
import os

from flask import Flask
from models import *
from helpers import read_csv_data

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def add_drivers_data():
    drivers_data = read_csv_data("data/drivers.csv")

    # Parse the csv data
    for row in drivers_data:
        driver = Driver(
            id=int(row[0]), 
            name=f"{row[4]} {row[5]}",
            code=row[3] if row[3] != "\\N" else None,
            number=int(row[2]) if row[2] != "\\N" else None, 
            dob=row[6], 
            nationality=row[7]
        )
        db.session.add(driver)

        print(f"Added {driver.name} to 'drivers'")

    # Commit the changes to the database
    db.session.commit()


def add_circuits_data():
    circuits_data = read_csv_data("data/circuits.csv")

    # Parse the csv data
    for row in circuits_data:
        circuit = Circuit(
            id=int(row[0]),
            name=row[2],
            location=row[3],
            country=row[4],
        )
        db.session.add(circuit)

        print(f"Added {circuit.name} to 'circuits'")

    # Commit the changes to the database
    db.session.commit()


def add_races_data():
    races_data = read_csv_data("data/races.csv")

    # Parse the csv data
    for row in races_data:
        race = Race(
            id=int(row[0]),
            name=row[4],
            circuit_id=int(row[3]),
            year=int(row[1]),
            sprint=False
        )
        db.session.add(race)

        print(f"Added {race.year} {race.circuit} to 'races'")
        
    # Commit the changes to the database
    db.session.commit()


def add_results_data():
    results_data = read_csv_data("data/results.csv")

    # Parse the csv data
    for row in results_data:
        result = Result(
            id=int(row[0]), 
            race_id=int(row[1]),
            driver_id=int(row[2]),
            position=int(row[6]) if row[6] != "\\N" else None,
            points=float(row[9])

        )
        db.session.add(result)

        print(f"Added {result.points} to {result.driver_id} in 'results'")
        
    # Commit the changes to the database
    db.session.commit()


# Run script to add the data
if __name__ == "__main__":
    with app.app_context():
        add_drivers_data()
        add_circuits_data()
        add_races_data()
        add_results_data()
