import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt
import pandas as pd

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Set Route
@app.route("/")
def home():

    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>" 
    )
################################################################################
@app.route("/api/v1.0/precipitation")
def r1():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query for prcp
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    
    # Create a dataframe to store the results
    prcp_df = pd.DataFrame(results, columns = ['date', 'prcp'])
    
    # Convert it to dictionary
    df = prcp_df.set_index('date')
    
    return df.to_dict()
##################################################################################
@app.route("/api/v1.0/stations")
def r2():    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query all station
    results = session.query(Station.station, Station.name).all()
    
    # Create a dictionary and loop all the each result into a new list
    station_results = []
    for station, name in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_results.append(station_dict)     

    session.close()    

    return jsonify(station_results)
#################################################################################
@app.route("/api/v1.0/tobs")
def r3():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query for prcp
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').all()

    session.close()
    
    # Create a dictionary and loop all the each result into a new list
    tobs_results = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temperature"] = tobs
        tobs_results.append(tobs_dict) 

    return jsonify(tobs_results)
###############################################################################
@app.route("/api/v1.0/<start>")
def r4(start):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query for prcp
    results = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()
    
    return jsonify(results)
###############################################################################
@app.route("/api/v1.0/<start>/<end>")
def r5(start, end):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query for prcp
    results = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
    
#########################################
# optimize
# 1. what if the date entered is not in datetime format?
# 2. how to add TMAX, TMIN and TAVG as key to the results?