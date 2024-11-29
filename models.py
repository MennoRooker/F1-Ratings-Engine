"""
Model classes for 'F1-ELO-Engine-2.0' repository
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

    def __init__(self, rating=0, **kwargs):
        super().__init__(**kwargs)  # Pass any SQLAlchemy column arguments to the parent class
        self.rating = rating
       

    def calc_rating(self, variables):
        self.rating = variables * self.rating
        return self.rating
    
    # Relationships
    results = db.relationship("Result", back_populates="driver")
    constructor = db.relationship("Constructor", back_populates="drivers")  # Link to the constructor


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


class Constructor(db.Model):
    __tablename__ = "constructors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ref = db.Column(db.String, nullable=False)

    # Relationships
    drivers = db.relationship("Driver", back_populates="constructor")  
    results = db.relationship("Result", back_populates="constructor")  


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


