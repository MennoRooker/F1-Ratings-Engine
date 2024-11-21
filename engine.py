"""
Flask application for books
"""

import os
import requests

from flask import Flask, render_template, session, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, joinedload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from models import *

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    # Query to filter results by the 2020 season
    results_2020 = (
        db.session.query(Result)
        .join(Race, Result.race_id == Race.id)
        .filter(Race.year == 2020)
        .options(joinedload(Result.driver))  # Eager load Driver relationship for better performance
        .all()
    )

    # Example: Print the driver, race, and points
    for result in results_2020:
        print(
            f"Driver: {result.driver.name}, "
            f"Race ID: {result.race_id}, "
            f"Points: {result.points}"
        )

# Run script to add the data
if __name__ == "__main__":
    with app.app_context():
        main()