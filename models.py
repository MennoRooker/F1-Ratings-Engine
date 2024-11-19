"""
Model classes for 'F1-ELO-Engine-2.0' repository
"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Driver(db.Model):
    __tablename__ = "drivers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=True)
    dob = db.Column(db.String, nullable=False)
    nationality = db.Column(db.String, nullable=False)

    def __init__(self, rating):
        self.rating = rating

    def calc_rating(self, variables):
        self.rating = variables * self.rating
        return self.rating
    
    # Relationship to results
    results = db.relationship("Result", back_populates="driver")


class Race(db.Model):
    __tablename__ = "races"

    id = db.Column(db.Integer, primary_key=True)
    circuit = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    sprint = db.Column(db.Boolean, nullable=False) # Indicates a sprint race

    # Relationship to results
    results = db.relationship("Result", back_populates="race")


class Result(db.Model):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey("races.id"), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)

    # Relationships
    race = db.relationship("Race", back_populates="results")
    driver = db.relationship("Driver", back_populates="results")

