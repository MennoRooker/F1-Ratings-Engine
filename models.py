"""
Model classes for 'F1-Ratings-Engine' repository
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Driver(db.Model):
    __tablename__ = "drivers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=True)
    number = db.Column(db.Integer, nullable=True)
    dob = db.Column(db.String, nullable=False)
    nationality = db.Column(db.String, nullable=False)
    constructor_id = db.Column(db.Integer, db.ForeignKey("constructors.id"), nullable=True)

    # Relationships
    results = db.relationship("Result", back_populates="driver")
    constructor = db.relationship("Constructor", back_populates="drivers")  # Link to the constructors table
    ratings = db.relationship("Rating", back_populates="driver")  # Link to the ratings table


class Circuit(db.Model):
    __tablename__ = "circuits"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)

    # Relationship to races
    races = db.relationship("Race", back_populates="circuit")


class Race(db.Model):
    __tablename__ = "races"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    circuit_id = db.Column(db.Integer, db.ForeignKey("circuits.id"), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    sprint = db.Column(db.Boolean, nullable=False) # Indicates a sprint race occurance

    # Relationships
    circuit = db.relationship("Circuit", back_populates="races")
    results = db.relationship("Result", back_populates="race")
    ratings = db.relationship("Rating", back_populates="race")


class Constructor(db.Model):
    __tablename__ = "constructors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ref = db.Column(db.String, nullable=False)

    # Relationships
    drivers = db.relationship("Driver", back_populates="constructor")  
    results = db.relationship("Result", back_populates="constructor")
    ratings = db.relationship("Rating", back_populates="constructor") 


class Result(db.Model):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey("races.id"), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)
    constructor_id = db.Column(db.Integer, db.ForeignKey("constructors.id"), nullable=True)
    position = db.Column(db.Integer, nullable=True)
    points = db.Column(db.Integer, nullable=False)

    # Relationships
    race = db.relationship("Race", back_populates="results")
    driver = db.relationship("Driver", back_populates="results")
    constructor = db.relationship("Constructor", back_populates="results") 


class Rating(db.Model):
    __tablename__ = "ratings"

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)
    constructor_id = db.Column(db.Integer, db.ForeignKey("constructors.id"), nullable=False)
    race_id = db.Column(db.Integer, db.ForeignKey("races.id"), nullable=False)
    year = db.Column(db.Integer, nullable=False) 
    points = db.Column(db.Float, nullable=False)
    adjusted_points = db.Column(db.Float, nullable=False)  # Corrected points after penalties
    zero_sum_rating = db.Column(db.Integer, nullable=False)  # Adds a zero-sum option for ranking

    # Relationships
    driver = db.relationship("Driver", back_populates="ratings")
    constructor = db.relationship("Constructor", back_populates="ratings")
    race = db.relationship("Race", back_populates="ratings")

# Add relationships to the relevant models
Driver.ratings = db.relationship("Rating", back_populates="driver", cascade="all, delete-orphan")
Constructor.ratings = db.relationship("Rating", back_populates="constructor", cascade="all, delete-orphan")
Race.ratings = db.relationship("Rating", back_populates="race", cascade="all, delete-orphan")


