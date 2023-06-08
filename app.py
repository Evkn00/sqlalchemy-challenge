from flask import Flask, jsonify

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas as pd
import datetime as dt

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Flask Setup
app = Flask(__name__)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#Flask Routes

## /
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

##Precipitation /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year ago from the latest date in the data set
    latest_date = session.query(func.max(Measurement.date)).scalar()
    date = dt.datetime.strptime(latest_date, "%Y-%m-%d")
    one_year_ago = date - dt.timedelta(days=365)

    # Query the date and precipitation values for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    # Close Session
    session.close()

    # Convert the query results to a dictionary with date as the key and prcp as the value
    precipitation_data = {}
    for date, prcp in results:
        precipitation_data[date] = prcp

    # Return the JSON representation of the precipitation data dictionary
    return jsonify(precipitation_data)

##Stations /api/v1.0/stations (Returns jsonified data of all of the stations in the database (3 points))


##Tobs /api/v1.0/tobs (Returns jsonified data for the most active station (USC00519281) (3 points)
## Only returns the jsonified data for the last year of data (3 points))


##/api/v1.0/<start>


##/api/v1.0/<start>/<end>

#Make runable from terminal
if __name__ == "__main__":
    app.run(debug=True)